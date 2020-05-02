#!/usr/bin/local/python
# -*- coding: utf-8 -*-

import os
import csv
import pandas as pd
from datetime import datetime
import pytest


class DataDictTable(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.new_file_path = 'new_%s.csv' %self.file_path.split('/')[-1].split('.')[0]

        raw_data = pd.read_csv(self.file_path)
        # print(raw_data)
        # print(raw_data.describe())
        nrow, ncol = raw_data.shape
        # print(nrow, ncol)
        self.df = raw_data

    def _write(self):
        pass

    def change_date(self):
        time_lst = self.df['报告日期']

        for (idx, time_) in enumerate(time_lst):
            # pytest.set_trace()
            # try:
            time_ = time_.split()[0]
            # pytest.set_trace()
            cday = datetime.strptime(time_, '%Y-%m-%d')

            new_data = cday.strftime('%Y%m%d')

            self.df['报告日期'][idx] = new_data
            # except Exception as error:
            #     print(error)
            #

    def change_age(self):
        age_lst = self.df['年龄']
        for (idx, age_) in enumerate(age_lst):
            if pd.isnull(age_):
                continue
            if age_ == 'nan':
                pytest.set_trace()
            age_ = age_.strip()
            if '岁' in age_:
                age_ = age_.strip('岁')
            elif '月' in age_:
                age_ = 0
            print(age_)
            self.df['年龄'][idx] = age_

    def change_date_2(self):
        time_lst = self.df['入院日期']
        for (idx, time_) in enumerate(time_lst):
            time_ = time_.split()[0]
            if time_[-2] == '9':
                year = '19'+ time_[-2:]
                time_ = time_[:-2] + year
                # time_ = time_.replace(time_[-2:], '19'+time_[-2:])
            elif time_[-2] in ['0', '1']:
                year = '20'+ time_[-2:]
                time_ = time_[:-2] + year
                # time_ = time_.replace(time_[-2:], '20'+time_[-2:])

            cday = datetime.strptime(time_, '%m/%d/%Y')

            new_data = cday.strftime('%Y%m%d')

            self.df['入院日期'][idx] = new_data
        pass

    def export_(self):
        self.df.to_csv(self.new_file_path)
        pass


class LightFile(DataDictTable):

    def __init__(self):
        super(LightFile, self).__init__()

    def read_file(self):
        data_lst = self._read()


def compare():
    star_path = "data0115/new_start_table.csv"
    little_path = "new_外院肾穿.csv"

    star_obj = DataDictTable(star_path)
    star_df = star_obj.df

    little_obj = DataDictTable(little_path)
    little_df = little_obj.df

    name_little_lst = little_df['姓名']
    name_star_lst = star_df['姓名']
    for each_name in name_little_lst:
        try:
            each_age = int(little_df.loc[little_df['姓名'] == each_name]['年龄'].values[0])
            each_gender = str(little_df.loc[little_df['姓名'] == each_name]['性别'].values[0])
            report_date = str(int(little_df.loc[little_df['姓名'] == each_name]['报告日期'].values[0]))

            form_rep_date = format_date(report_date)
        except Exception:
            pytest.set_trace()

        if each_name in name_star_lst.values:
            counts_name = int(name_star_lst.value_counts()[each_name])
            if counts_name == 1:
                # print("---", each_name)
                # pytest.set_trace()

                star_age = int(star_df.loc[star_df['姓名'] == each_name]['年龄'].values[0])
                star_gender = star_df[star_df['姓名'] == each_name]['性别'].values[0]
                admission_date = str(int(star_df[star_df['姓名'] == each_name]['入院日期'].values[0]))
                form_adm_date = format_date(admission_date)

                date_delta = form_rep_date.__sub__(form_adm_date).days

                if each_age == star_age and each_gender == star_gender and date_delta <= 60:
                    pass
                else:
                    # print("ddddd", each_name)
                    pass

            else:
                whole_df = star_df.loc[star_df['姓名'] == each_name]
                for index, row in whole_df.iterrows():
                    age_ = int(row['年龄'])
                    gender_ = str(row['性别'])
                    adm_date_ = str(row['入院日期'])
                    form_adm_date = format_date(adm_date_)
                    date_delta = form_rep_date.__sub__(form_adm_date).days
                    if each_age == age_ and each_gender == gender_ and date_delta <= 60:
                        pass
                        print("-,-", each_name)
                    else:
                        # print("ccc", each_name)
                        pass

                # if each_age in star_df.loc[star_df['姓名'] == each_name]['年龄'].values:
                #     print(star_df.loc[star_df['姓名'] == each_name]['年龄'].values)
                #     if each_gender in star_df.loc[star_df['姓名'] == each_name]['性别'].values:
                #         print("-,-", each_name)

        else:
            # print("doesn't exist", each_name)
            pass


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