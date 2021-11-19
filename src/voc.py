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
):
    img_files = []
    for img in img_list:
        p = PurePath(img)
        p = str(p.parts[-1])  # p == file name like '970.jpg'
        img_files.append(p)
    for anno in label_list:
        xml_obj = xml_load(anno)
        image_info = get_image_info_xml(xml_obj)
        if not (image_info["file_name"] in img_files):
            raise ImageException(
                f"{image_info['file_name']} is not in dataset, check your files"
            )
        for obj in xml_obj.findall("object"):
            xmin, ymin, xmax, ymax = get_bbox_from_xml_obj(obj, label2id, anno)
            if xmax <= xmin or ymax <= ymin:
                raise LabelException(
                    f"Box size error in {os.path.basename(anno)}: (xmin, ymin, xmax, ymax): {xmin, ymin, xmax, ymax}"
                )
            if image_info["width"] < xmax:
                raise LabelException(
                    f"Box size error in {os.path.basename(anno)}: xmax: {xmax} is greater than 'width'"
                )
            if image_info["height"] < ymax:
                raise LabelException(
                    f"Box size error in {os.path.basename(anno)}: ymax: {ymax} is greater than 'height'"
                )
            if xmin <= 0:
                raise LabelException(
                    f"Box size error in {os.path.basename(anno)}: xmin: {xmin} is negative value."
                )
            if ymin <= 0:
                raise LabelException(
                    f"Box size error in {os.path.basename(anno)}: ymin: {ymin} is negative value."
                )
            if xmax <= 0:
                raise LabelException(
                    f"Box size error in {os.path.basename(anno)}: xmax: {xmax} is negative value."
                )
            if ymax <= 0:
                raise LabelException(
                    f"Box size error in {os.path.basename(anno)}: ymax: {ymax} is negative value."
                )


def validate(dir_path: str, num_classes: int, label_list:List[str], img_list:List[str]):
    label2id = get_label2id(label_list, num_classes)
    if len(label2id) != num_classes:
        raise LabelException(
            f"'num_classes' is not matched with number of classes in your datasets. Number of classes in your dataset is {len(label2id)}"
        )
    validate_image_files_exist(img_list, label_list, "xml")
    print("[Validate: 5/6]: Done validation for exsisting images files in correct position.")
    validate_label_files(img_list, label_list, num_classes, label2id)
    print("[Validate: 6/6]: Done validation for each label files.")
