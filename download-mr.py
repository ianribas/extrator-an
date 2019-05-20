#!/usr/bin/env python3
# -*- coding: UTF-8
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
from urllib.request import urlretrieve
import os.path
import csv


if __name__ == "__main__":
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        print('Usage: download-mr.py [csv]')

    with open(fname, newline='') as f:
        reader = csv.reader(f)
        print('reader', reader)
        for row in reader:
            filename = row[1]
            flink = row[2]
            if flink != '--' and not os.path.isfile(filename):
                urlretrieve(flink, filename)
                print('Carregou arquivo:', filename)

