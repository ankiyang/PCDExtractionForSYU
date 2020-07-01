#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-

import os
import csv
import copy
import pandas as pd
from datetime import datetime
import pytest

from com import DataDictTable


def change_elec_date():
    path = "电镜集合/电镜csv/电镜change_date.csv"
    elec_dd = DataDictTable(path)
    elec_dd.change_date_2()
    elec_dd.change_age()
    elec_dd.export_()


def compare():
    star_path = "data0115/new_start_table.csv"
    little_path = "data0115/new_外院肾穿.csv"

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


if __name__ == '__main__':
    change_elec_date()
    pass