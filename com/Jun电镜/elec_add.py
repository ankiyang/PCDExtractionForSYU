#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-


import copy
from datetime import datetime
import pytest

from com import DataDictTable
import pandas as pd


def format_date(date_string):
    try:
        date_obj = datetime.strptime(date_string, '%Y%m%d')
    except:
        pytest.set_trace()
    return date_obj


def fill_col(little_df, start_df, star_num):
    try:
        if start_df.loc[start_df['编号'] == star_num, "电镜"].isnull().any() or \
                not start_df.loc[start_df['编号'] == star_num, "电镜"][star_num].strip():
            start_df.loc[start_df['编号'] == star_num, "电镜"] = little_df["电镜"]
            start_df.loc[start_df['编号'] == star_num, "电镜报告日期"] = little_df['报告日期']
        if (start_df.loc[start_df['编号'] == star_num, "入院诊断"]).isnull().any():
            start_df.loc[start_df['编号'] == star_num, "入院诊断"] = little_df["入院诊断"]

        print('fill.', little_df['姓名'])
    except:
        print("error")
        pytest.set_trace()
    return start_df


def add_new_lines(row, added_df):
    # 添加新的一行到新的表里面
    try:

        print('add.', row['姓名'])
        new_df = added_df.append(row, ignore_index=True)
    except:
        pytest.set_trace()
    return new_df


def compare():
    star_path = "无电镜数据v3.csv"
    little_path = "new_电镜.csv"

    star_obj = DataDictTable(star_path)
    star_df = star_obj.df
    star_df['编号'] = range(len(star_df['编号']))

    new_star_df = copy.deepcopy(star_df)

    little_obj = DataDictTable(little_path)
    little_df = little_obj.df

    added_elec_df = pd.DataFrame(data=None, columns=little_df.columns.values)
    for _, each_row in little_df.iterrows():
        each_name = str(each_row['姓名'])
        star_cor_df = star_df.loc[star_df['姓名'] == each_name]

        if not star_cor_df.empty:
            try:
                # 电镜表的那一列数据
                little_each_age = int(each_row['年龄'])
                little_each_gender = str(each_row['性别']).strip()
                little_report_date = str(int(each_row['报告日期'])).strip()
                little_each_form_rep_date = format_date(little_report_date)
                little_bingan = str(each_row['病案号']).strip()
            except:
                pytest.set_trace()

            if star_cor_df.shape[0] == 1:

                star_row = star_cor_df.iloc[0]

                #  星星表对应的那一列数据
                number_ = int(star_row['编号'])
                star_age = int(star_row['年龄'])
                star_gender = str(star_row['性别']).strip()
                admission_date = str(star_row['入院日期']).strip()
                report_date = str(star_row['报告日期']).strip()
                star_jizhang = str(star_row['记帐号']).strip()

                if little_bingan != 'nan' and star_jizhang != 'nan':
                    little_bingan = int(float(little_bingan))
                    star_jizhang = int(float(star_jizhang))
                    if little_bingan == star_jizhang:
                        new_star_df = fill_col(each_row, new_star_df, number_)
                        continue
                else:
                    pass

                if admission_date == "nan" and report_date == "nan":
                    added_elec_df = add_new_lines(each_row, added_elec_df)
                else:
                    # 如果入院日期有的话，先定为入院日期
                    if admission_date != "nan":
                        date_ = admission_date
                    # 如果有报告日期，先定为报告日期
                    else:
                        date_ = report_date

                    form_date_ = format_date(date_)
                    date_delta = little_each_form_rep_date.__sub__(form_date_).days
                    if abs(little_each_age - star_age) <= 2 \
                            and little_each_gender == star_gender \
                            and 0 <= date_delta <= 120:
                        new_star_df = fill_col(each_row, new_star_df, number_)
                    else:
                        added_elec_df = add_new_lines(each_row, added_elec_df)

            else:
                # if_find = False
                match_res = list()
                for index, star_row in star_cor_df.iterrows():
                    age_ = int(star_row['年龄'])
                    gender_ = str(star_row['性别']).strip()
                    adm_date = str(star_row['入院日期']).strip()
                    rep_date = str(star_row['报告日期']).strip()
                    jizhang_ = str(star_row['记帐号']).strip()

                    if little_bingan != "nan" and jizhang_ != "nan":
                        try:
                            little_bingan = int(float(little_bingan))
                            jizhang_ = int(float(jizhang_))
                            if little_bingan == jizhang_:
                                match_res.append(True)
                                continue
                        except:
                            pytest.set_trace()
                    else:
                        pass

                    if adm_date == "nan" and adm_date == "nan":
                        match_res.append(False)
                    else:
                        if adm_date != "nan":
                            date_ = adm_date
                        else:
                            date_ = rep_date

                        form_date_ = format_date(date_)
                        date_delta = little_each_form_rep_date.__sub__(form_date_).days

                        if abs(little_each_age - age_) <= 2 and little_each_gender == gender_ \
                                and 0 <= date_delta <= 120:
                            match_res.append(True)
                        else:
                            match_res.append(False)
                if True not in match_res:
                    added_elec_df = add_new_lines(each_row, added_elec_df)
                else:
                    if match_res.count(True) == 1:
                        idx = match_res.index(True)
                        row = star_cor_df.iloc[idx]
                        new_star_df = fill_col(each_row, new_star_df, int(row['编号']))
                    else:
                        print("!!!!")
                        pytest.set_trace()

        else:
            added_elec_df = add_new_lines(each_row, added_elec_df)
            pass

    new_star_df['年龄'] = new_star_df['年龄'].astype(int)
    added_elec_df['年龄'] = added_elec_df['年龄'].astype(int)
    pytest.set_trace()

    added_elec_df.to_csv('电镜没匹配到的数据表.csv', index=False)
    new_star_df.to_csv('导入了电镜的大表.csv', index=False)


if __name__ == '__main__':
    compare()