import glob
import os
import shutil
import sys
import zipfile
from pathlib import Path, PurePath, PurePosixPath
from typing import Dict, List

import yaml

from src.utils import (get_file_lists, replace_images2labels,
                       validate_data_yaml, validate_dataset_type,
                       validate_first_dirs, validate_image_files_exist,
                       validate_second_dirs, yaml_safe_load)


def validate_label_files(label_list: List[str], num_classes: int, errors:List[str]):
    for ll in label_list:
        with open(ll, "r") as f:
            line = f.readlines()
            ret_file_name = "/".join(ll.split("/")[4:])
            line_number = 0
            for l in line:
                line_number += 1
                label = l.split("\n")
                values = label[0].split(" ")
                if type(int(values[0])) != int:
                    errors.append(
                        f"{ll} has wrong class number in line {line_number}."
                    )
                if (int(values[0]) >= num_classes) or (int(values[0]) < 0):
                    errors.append(
                        f"{ll} has wrong class number {values[0]} in line {line_number}."
                    )
                for v in values[1:]:
                    if (float(v) > 1) or (float(v) <= 0):
                        errors.append(
                            f"{ll} has wrong coordinate value in line {line_number}."
                        )
    return errors


def validate(
    dir_path: str, 
    num_classes: int, 
    label_list:List[str], 
    img_list:List[str],
    yaml_path:None,
    errors:List[str]
):
    errors = validate_image_files_exist(img_list, label_list, "txt", errors)
    print("[Validate: 5/6]: Done validation for exsisting images files in correct position.")
    errors = validate_label_files(label_list, num_classes, errors)
    print("[Validate: 6/6]: Done validation for each label files.")
    return errors