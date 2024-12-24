#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   test_read_yolo.py
@Time    :   2024/12/09 15:44:53
@Author  :   firstElfin 
@Version :   1.0
@Desc    :   None
'''
import os
import sys
from pathlib import Path


FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from codeUtils.labelOperation.readLabel import read_yolo
from codeUtils.labelOperation.labelme2other import labelme2yolo


a = read_yolo('test/yolo_test.txt')
print(a)
labelme2yolo(
    labelme_json_dir="./labelme_jsons", 
    yolo_save_dir="./labelme_jsons",
    cls_ids="/Users/elfin/project/codeTools/labelme_jsons/classes.txt"
)