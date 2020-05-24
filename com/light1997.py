#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-

import copy
from datetime import datetime
import pytest

from com import DataDictTable


def format_date(date_string):
    date_obj = datetime.strptime(date_string, '%Y%m%d')
    return date_obj


def change_elec_date():
    path = "data0115/光镜/2018-17/08-17年光镜.csv"
    elec_dd = DataDictTable(path)
    elec_dd.change_date()
    elec_dd.change_age()
    elec_dd.export_()


def compare():
    star_path = "要弄电镜的/star_肾穿_97_06_08.csv"
    little_path = "光镜集合/new_2017-now.csv"

    star_obj = DataDictTable(star_path)
    star_df = star_obj.df
    star_cp_df = copy.deepcopy(star_df)

    little_obj = DataDictTable(little_path)
    little_df = little_obj.df

    for _, each_row in little_df.iterrows():
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
                if admission_date == "nan":
                    pytest.set_trace()
                form_adm_date = format_date(admission_date)
                date_delta = little_each_form_rep_date.__sub__(form_adm_date).days

                if abs(little_each_age - star_age) <= 1 \
                        and little_each_gender == star_gender \
                        and 0 < date_delta <= 60:
                    fill_col(each_row, star_cp_df, each_name)
                else:
                    star_cp_df = add_new_lines(each_row, star_cp_df)
            else:
                if_find = False
                for index, star_row in star_cor_df.iterrows():
                    try:
                        age_ = int(star_row['年龄'])
                        gender_ = str(star_row['性别'])
                        adm_date_ = str(int(star_row['入院日期']))
                        form_adm_date = format_date(adm_date_)
                        date_delta = little_each_form_rep_date.__sub__(form_adm_date).days
                    except:
                        pytest.set_trace()

                    if abs(little_each_age - age_) <= 1 \
                            and little_each_gender == gender_ \
                            and 0 < date_delta <= 60:
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

    star_cp_df.to_csv('star_肾穿_97_06_08_17.csv', index=False)


def fill_col(little_df, start_df, each_name, each_age=None, each_gender=None, each_date=None):
    try:
        field_lst = ['报告日期', '光镜+免疫荧光']
        # if little_df['电镜']:
        #     field_lst.append('电镜')

        for fill_field in field_lst:
            if each_age and each_gender and each_date:
                start_df.loc[(start_df['姓名'] == each_name) & (start_df['年龄'] == each_age)
                             & (start_df['性别'] == each_gender) & (start_df['入院日期'] == each_date),
                             fill_field] = little_df[fill_field]
            else:
                start_df.loc[start_df['姓名'] == each_name, fill_field] = little_df[fill_field]
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
    try:
        date_obj = datetime.strptime(date_string, '%Y%m%d')
    except:
        pytest.set_trace()
    return date_obj


if __name__ == '__main__':
    # change_elec_date()
    compare()