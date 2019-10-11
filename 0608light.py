#!/usr/bin/local/python3.6
# -*- coding: utf-8 -*-

import csv
from docx import Document
from electron_microscope import elec_lines
from test import FileHandler

res_dict = dict()


class LightHandler(FileHandler):

    def __init__(self, file_path):
        super().__init__(file_path)

    def parsing_word(self):
        f = Document(self.file_path)

        tem_lst = list()

        for para in f.paragraphs:
            line_context = para.text

            if r'病理号' in line_context:
                case_handler = CaseHandler(tem_lst)
                case_handler.dealing_()
                print(case_handler.attr_dict)
                case_handler.line_creation()

                tem_lst = list()

            elif not line_context:
                continue
            tem_lst.append(line_context)


class CaseHandler(object):

    def __init__(self, case_lst):
        self.case_lst = case_lst
        self.attr_lst = ['pathology_number',  # 病理号
                         'name',  # 姓名
                         'gender',  # 性别
                         'age',  # 年龄
                         'clinical_diagnosis',  # 临床诊断
                         'hospital',  # 送检医院
                         'inpatient_area',  # 病区
                         'admission_number',  # 住院号
                         'report_date',  #报告日期
                         'pathological_report',  # 病理报告
                         'elec_info' # 电镜报告
                         ]
        self.attr_dict = dict()

    def line_creation(self):
        if not self.attr_dict:
            return
        line = [self.attr_dict[at] for at in self.attr_lst]
        out = open('result0608.csv', 'a', newline='')
        csv_write = csv.writer(out, dialect='excel')
        csv_write.writerow(line)
        out.close()

    def check_repe(self):
        electron_info = elec_lines()
        light_name_number = "%s,%s" % (self.attr_dict['name'], self.attr_dict['admission_number'])
        if light_name_number in electron_info :
            self.attr_dict['elec_info'] = electron_info[light_name_number][-1]

        file = open("repeat_record.txt", encoding="utf-8", mode="a")
        file.write(light_name_number)
        file.close()

    def dealing_(self):
        basic_info_lst = [r'姓名', r'性别', r'年龄', r'住院号']
        hos_info_lst = [r'医院', r'病区', r'临床诊断']

        if not self.case_lst:
            return
        self.attr_dict.setdefault('report_date', "")
        self.attr_dict.setdefault('elec_info', "")

        self.attr_dict['pathology_number'] = self.case_lst[0].split()[0].split(':')[-1]

        basic_info = self.case_lst[2]
        if all([info in basic_info for info in basic_info_lst]):
            self.attr_dict['name'] = basic_info.split()[0].split(':')[-1]
            self.attr_dict['gender'] = basic_info.split()[1].split(':')[-1]
            self.attr_dict['age'] = basic_info.split()[2].split(':')[-1]
            self.attr_dict['admission_number'] = basic_info.split()[3].split(':')[-1]
        else:
            return

        hos_info = self.case_lst[3]
        print(hos_info)
        if all([info in hos_info for info in hos_info_lst]):
            _index_diagnosis = hos_info.index(r'临床诊断:')
            self.attr_dict['hospital'] = hos_info.split()[0].split(':')[-1]
            self.attr_dict['inpatient_area'] = hos_info.split()[2].split(':')[-1]
            self.attr_dict['clinical_diagnosis'] = hos_info[_index_diagnosis+5:].split()[0]

        pathology_index = [i for i,s in enumerate(self.case_lst) if r'病理报告:' in s][0]
        reporter_index = [i for i,s in enumerate(self.case_lst) if '报告者' in s][0]
        self.attr_dict['pathological_report'] = '\n'.join(self.case_lst[pathology_index+1:reporter_index])

        report_date_line = self.case_lst[reporter_index]
        report_date_index = report_date_line.index('报告日期:')
        report_date_lst = report_date_line[report_date_index+5:].split('-')
        self.attr_dict['report_date'] = '%s年%s月%s日'% (report_date_lst[0], report_date_lst[1], report_date_lst[2])

        elec_index = [i for i,s in enumerate(self.case_lst) if r'电镜报告:' in s]
        if elec_index:
            elec_index = elec_index[0]
            elec_report_index = [i for i,s in enumerate(self.case_lst) if r'电镜报告者' in s][0]
            self.attr_dict['elec_info'] = '\n'.join(self.case_lst[elec_index+2:elec_report_index-1])


def deal_file(file_path):
    fh = LightHandler(file_path)
    fh.parsing_word()


if __name__ == '__main__':
    deal_file('')
    pass

