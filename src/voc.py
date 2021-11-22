import glob
import os
import shutil
import sys
import zipfile
from pathlib import Path, PurePath, PurePosixPath
from typing import Dict, List

import yaml

from src.utils import (get_bbox_from_xml_obj, get_file_lists,
                                      get_image_info_xml, get_label2id,
                                      replace_images2labels,
                                      validate_data_yaml,
                                      validate_dataset_type,
                                      validate_first_dirs,
                                      validate_image_files_exist,
                                      validate_second_dirs, xml_load)


def validate_label_files(
    img_list: List[str],
    label_list: List[str],
    num_classes: int,
    label2id: Dict[str, int],
    errors: List[str]
):
    for anno in label_list:
        xml_obj = xml_load(anno)
        image_info = get_image_info_xml(xml_obj)
        for obj in xml_obj.findall("object"):
            xmin, ymin, xmax, ymax, errors = get_bbox_from_xml_obj(obj, label2id, anno, errors)
            if xmax <= xmin or ymax <= ymin:
                errors.append(
                    f"Box size error in {anno}: (xmin, ymin, xmax, ymax): {xmin, ymin, xmax, ymax}."
                )
            if image_info["width"] < xmax:
                errors.append(
                    f"Box size error in {anno}: xmax: {xmax} is greater than 'width'."
                )
            if image_info["height"] < ymax:
                errors.append(
                    f"Box size error in {anno}: ymax: {ymax} is greater than 'height'."
                )
            if xmin <= 0:
                errors.append(
                    f"Box size error in {anno}: xmin: {xmin} is negative value."
                )
            if ymin <= 0:
                errors.append(
                    f"Box size error in {anno}: ymin: {ymin} is negative value."
                )
            if xmax <= 0:
                errors.append(
                    f"Box size error in {anno}: xmax: {xmax} is negative value."
                )
            if ymax <= 0:
                errors.append(
                    f"Box size error in {anno}: ymax: {ymax} is negative value."
                )
    return errors


def validate_yaml_names(yaml_label:List[str], label2id:Dict[str, int], num_classes:int, errors:List[str]):
    for y in yaml_label:
        if y not in label2id.keys():
            errors.append(
                f"{y} is not in xml files. Class names in 'data.yaml' have to match with xml files. Please check 'data.yaml' and xml files. Class names in xml files are {list(label2id.keys())}.")

    if len(label2id) != num_classes:
        errors.append(
            f"'num_classes' is not matched with the number of classes in your datasets. The number of classes in dataset is {len(label2id)}. Class names in xml files are {list(label2id.keys())}."
        )
    return errors


def validate(
    dir_path: str, 
    num_classes: int, 
    label_list:List[str], 
    img_list:List[str], 
    yaml_label:List[str],
    errors:List[str]
    ):
    label2id = get_label2id(label_list, num_classes)
    errors = validate_yaml_names(yaml_label, label2id, num_classes, errors)
    errors = validate_image_files_exist(img_list, label_list, "xml", errors)
    print("[Validate: 5/6]: Validation finished for existing image files in the correct position.")
    errors = validate_label_files(img_list, label_list, num_classes, label2id, errors)
    print("[Validate: 6/6]: Validation finished for label files.")
    return errors