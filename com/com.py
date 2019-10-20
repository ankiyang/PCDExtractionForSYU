#!/usr/bin/local/python
# -*- coding: utf-8 -*-

import os
import csv


def comp(f1, f2):
    pass


class DataDictTable(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.new_file_path = os.path.join(os.path.split(self.file_path)[0], "new_.csv")

    def _read(self):
        with open(self.file_path, newline="") as f:
            reader = csv.reader(f, delimiter='')
            for row in reader:
                print(row)

    def _write(self):
        pass


class StarFile(DataDictTable):

    def __init__(self):
        super(StarFile, self).__init__()

    def read_file(self):
        pass



if __name__ == '__main__':
    pass