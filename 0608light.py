#!/usr/bin/local/python3.6
# -*- coding: utf-8 -*-

import os
import json
import csv
import time
import re
from docx import Document
from electron_microscope import elec_lines
from docx.shared import Inches
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

                tem_lst = list()

            elif not line_context:
                continue
            tem_lst.append(line_context)


class CaseHandler(object):

    def __init__(self, case_lst):
        self.case_lst = case_lst

    def dealing_(self):
        if not self.case_lst:
            return
        print(self.case_lst)
        pass


def deal_file(file_path):
    fh = LightHandler(file_path)
    fh.parsing_word()


if __name__ == '__main__':
    deal_file('')
    pass

