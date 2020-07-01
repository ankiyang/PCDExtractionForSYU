#!/usr/bin/local/python
# -*- coding: utf-8 -*-

import os
import csv
import copy
import pandas as pd
from datetime import datetime
import pytest
import re

class DataDictTable(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.new_file_path = 'new_%s.csv' %self.file_path.split('/')[-1].split('.')[0]

        raw_data = pd.read_csv(self.file_path, dtype={'入院日期':str, '报告日期':str})
        # print(raw_data)
        # print(raw_data.describe())
        nrow, ncol = raw_data.shape
        # print(nrow, ncol)
        self.df = raw_data

    def _write(self):
        pass

    def change_date(self):
        # change date 2000-12-01 --> 20001201
        time_lst = self.df['报告日期']

        for (idx, time_) in enumerate(time_lst):
            # pytest.set_trace()
            time_ = time_.split()[0]
            cday = datetime.strptime(time_, '%Y-%m-%d')
            new_data = cday.strftime('%Y%m%d')

            self.df['报告日期'][idx] = new_data

    def change_age(self):
        age_lst = self.df['年龄']
        for (idx, age_) in enumerate(age_lst):
            if pd.isnull(age_):
                pytest.set_trace()
            age_ = str(age_)
            if '岁' in age_:
                age_ = age_.strip('岁')
            elif '月' in age_ or '天' in age_:
                age_ = 0
            age_ = age_.strip()

            self.df['年龄'][idx] = age_

    def change_date_2(self):
        # change date 12/01/2000 -> 20001201
        time_lst = self.df['报告日期']
        try:
            for (idx, time_) in enumerate(time_lst):
                time_ = time_.split()[0]
                # if time_[-2] == '9':
                #     year = '19' + time_[-2:]
                #     time_ = time_[:-2] + year
                # elif time_[-2] in ['0', '1', '2']:
                #     year = '20' + time_[-2:]
                #     time_ = time_[:-2] + year
                # else:
                #     pytest.set_trace()

                cday = datetime.strptime(time_, '%Y/%m/%d')
                new_data = cday.strftime('%Y%m%d')

                self.df['报告日期'][idx] = new_data
        except:
            pytest.set_trace()
        pass

    def change_date_3(self):
        time_lst = self.df['报告日期']
        try:
            for (idx, time_) in enumerate(time_lst):
                time_ = time_.split()[0]
                # pytest.set_trace()
                cday = datetime.strptime(time_, '%Y年%m月%d日')
                new_data = cday.strftime('%Y%m%d')

                self.df['报告日期'][idx] = new_data
        except:
            pytest.set_trace()

    def export_(self):
        self.df.to_csv(self.new_file_path, index=False)
        pass


class LightFile(DataDictTable):

    def __init__(self):
        super(LightFile, self).__init__()

    def read_file(self):
        data_lst = self._read()


def compare():
    star_path = "data0115/new_start_table.csv"
    little_path = "肾穿集合/new_外院肾穿.csv"

    star_obj = DataDictTable(star_path)
    star_df = star_obj.df
    star_cp_df = copy.deepcopy(star_df)

    little_obj = DataDictTable(little_path)
    little_df = little_obj.df

    for _, each_row in little_df.iterrows():
        # pytest.set_trace()
        each_name = str(each_row['姓名'])
        star_cor_df = star_df.loc[star_df['姓名'] == each_name]

        try:
            little_each_age = int(each_row['年龄'])
            little_each_gender = str(each_row['性别'])
            little_report_date = str(int(each_row['报告日期']))
            little_each_form_rep_date = format_date(little_report_date)
        except:
            pytest.set_trace()

        if not star_cor_df.empty:
            if star_cor_df.shape[0] == 1:
                star_row = star_cor_df.iloc[0]

                star_age = int(star_row['年龄'])
                star_gender = str(star_row['性别'])
                admission_date = str(star_row['入院日期'])
                form_adm_date = format_date(admission_date)
                date_delta = little_each_form_rep_date.__sub__(form_adm_date).days

                if abs(little_each_age - star_age) <= 1 \
                        and little_each_gender == star_gender \
                        and date_delta <= 60:
                    fill_col(each_row, star_cp_df, each_name)
                else:
                    star_cp_df = add_new_lines(each_row, star_cp_df)
            else:
                if_find = False
                for index, star_row in star_cor_df.iterrows():
                    age_ = int(star_row['年龄'])
                    gender_ = str(star_row['性别'])
                    adm_date_ = str(int(star_row['入院日期']))
                    form_adm_date = format_date(adm_date_)
                    date_delta = little_each_form_rep_date.__sub__(form_adm_date).days

                    if abs(little_each_age - age_) <= 1 \
                            and little_each_gender == gender_ \
                            and date_delta <=60:
                        fill_col(each_row, star_cp_df, each_name,
                                 each_age=age_, each_gender=gender_, each_date=adm_date_)
                        if_find = True
                        break
                    else:
                        continue
                if not if_find:
                    star_cp_df = add_new_lines(each_row, star_cp_df)
                pass
        else:
            star_cp_df = add_new_lines(each_row, star_cp_df)
            pass
    pytest.set_trace()


def export_(df):
    df.to_csv('new_star_shenchuan.csv', index=False)
    pass


def fill_col(little_df, start_df, each_name, each_age=None, each_gender=None, each_date=None):
    try:
        if each_age and each_gender and each_date:
            start_df.loc[(start_df['姓名'] == each_name)
                         & (start_df['年龄'] == each_age)
                         & (start_df['性别'] == each_gender)
                         & (start_df['入院日期'] == each_date),
                         '光镜+免疫荧光'] = little_df['光镜+免疫荧光']
        start_df.loc[start_df['姓名'] == each_name, '光镜+免疫荧光'] = little_df['光镜+免疫荧光']
        start_df.loc[start_df['姓名'] == each_name, '报告日期'] = little_df['报告日期']
        print('fill.', each_name)
    except:
        pytest.set_trace()
    return start_df


def add_new_lines(little_df, star_df):
    # 添加新的一行
    try:
        print('add.', little_df['姓名'])
        new_df = star_df.append(little_df, ignore_index=True)
    except:
        pytest.set_trace()

    return new_df


def format_date(date_string):
    date_obj = datetime.strptime(date_string, '%Y%m%d')
    return date_obj

    pass


def test():
    ddt = DataDictTable("start_table.csv")
    ddt.change_date_2()
    # ddt.change_age()
    ddt.export_()


if __name__ == '__main__':
    compare()
    # test()