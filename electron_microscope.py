#!/usr/bin/local/python
# -*- coding: utf-8 -*-

import json
import csv

repeat_info = dict()


def elec_handle():
    light_dict = json_()
    with open('elecinfo.csv', 'r', encoding='utf-8') as f:
        f_csv = csv.reader(f,dialect='excel')
        for row in f_csv:

            name = row[0].strip().replace(" ", "")
            admission_number = row[6].strip()
            elec_result = row[-1]
            test_key = "%s,%s" % (name, admission_number)
            if test_key in light_dict.keys():
                pathology_number = light_dict[test_key]
                repeat_info[pathology_number] = elec_result


def elec_lines():
    elec_info = dict()
    with open('elecinfo.csv', 'r',  encoding='utf-8') as f:
        f_csv = csv.reader(f, dialect='excel')
        for row in f_csv:

            name = row[0].strip().replace(" ", "")
            gender = row[1]
            age = row[2]
            hospital = row[3]
            inpatient_area = row[4]
            admission_number = row[6]
            clinical_diagnosis = row[7]
            pathology_number = row[9]
            report_date = row[10]
            elec_diag = row[-1].strip()
            elec_info["%s,%s" % (name, admission_number)] = \
                [pathology_number, name, gender, age, "", clinical_diagnosis,
                 hospital, inpatient_area, admission_number, report_date, "", "",
                 "", "", "", "", "", "", "",
                 elec_diag]
    return elec_info


def write_elecinfo():
    pass


def json_():
    with open("nn.json", 'r') as fw:
        load_dict = json.load(fw)
    return load_dict


if __name__ == '__main__':
    # print(json_())
    print(elec_lines())