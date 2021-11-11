import glob
import os
import shutil
import sys
import zipfile
from pathlib import Path, PurePath, PurePosixPath
from typing import Dict, List

import yaml

from src.exceptions import (DirectoryException, ImageException,
                                   LabelException, YamlException)
from src.utils import (get_file_lists, replace_images2labels,
                                      validate_data_yaml, validate_first_dirs,
                                      validate_image_files_exist,
                                      validate_second_dirs, yaml_safe_load)


def validate_label_files(label_list: List[str], num_classes: int):
    for ll in label_list:
        error_file_name = Path(ll).parts[-1]
        f = open(ll, "r")
        line = f.readlines()
        ret_file_name = "/".join(ll.split("/")[4:])
        for l in line:
            label = l.split("\n")
            values = label[0].split(" ")
            if type(int(values[0])) != int:
                raise LabelException(
                    f"Label file {error_file_name} has wrong class number, check your file"
                )
            if (int(values[0]) >= num_classes) or (int(values[0]) < 0):
                raise LabelException(
                    f"Label file {error_file_name} has wrong class number {values[0]}, check your file"
                )
            for v in values[1:]:
                if (float(v) > 1) or (float(v) <= 0):
                    raise LabelException(
                        f"Label file {error_file_name} has wrong coordinate value, check your file"
                    )


def validate(root_path: str, num_classes: int, delete=False):
    dir_path = Path(root_path)
    dir_paths = validate_first_dirs(dir_path)
    validate_second_dirs(dir_paths)
    img_list, label_list = get_file_lists(dir_paths)
    validate_data_yaml(dir_path, num_classes)
    validate_image_files_exist(img_list, label_list, "txt")
    validate_label_files(label_list, num_classes)
    if delete:
        delete_dirs(dir_path)


if __name__ == "__main__":
    validate("devtest/zip2_yolo", "zip2_yolo", 11)
