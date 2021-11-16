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
from src.utils import (does_it_have, get_dir_list,
                                      get_file_lists, get_target_dirs,
                                      json_load, validate_data_yaml,
                                      validate_first_dirs,
                                      validate_second_dirs,
                                      validate_dataset_type)


def validate_coco_bbox(bbox: List[float], width: float, height: float):
    x, y, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
    if not width >= x + w:
        raise LabelException(
            "Image file's width can not be smaller than 'x'+'width' in bbox, check your label file"
        )
    if not height >= y + h:
        raise LabelException(
            "Image file's height can not be smaller than 'y'+'height' in bbox, check your label file"
        )
    if not x >= 0:
        raise LabelException(
            "'x in bbox can not be negative value, check your label file"
        )
    if not y >= 0:
        raise LabelException(
            "'y in bbox can not be negative value, check your label file"
        )
    if not w >= 0:
        raise LabelException(
            "width in bbox can not be negative value, check your label file"
        )
    if not h >= 0:
        raise LabelException(
            "height in bbox can not be negative value, check your label file"
        )
    if not width >= x:
        raise LabelException(
            "'width can not be smaller than 'x' in bbox, check your label file"
        )
    if not height >= y:
        raise LabelException(
            "'height can not be smaller than 'y' in bbox, check your label file"
        )


def validate_coco_label(
    images: List[Dict], annotations: List[Dict], json_file_name: str, max_classes: int
):
    class_ids = []
    for img in images:
        if img.get("id") is None:
            raise LabelException(
                f"There is not 'id' in 'images' in file {json_file_name}, check your label file"
            )
        if img.get("file_name") is None:
            raise LabelException(
                f"There is not 'file_name' in 'images' in file {json_file_name}, check your label file"
            )
        if img.get("height") is None:
            raise LabelException(
                f"There is not 'height' in 'images' in file {json_file_name}, check your label file"
            )
        if img.get("width") is None:
            raise LabelException(
                f"There is not 'width' in 'images' in file {json_file_name}, check your label file"
            )
    for anno in annotations:
        if anno.get("id") is None:
            raise LabelException(
                f"There is not 'id' in 'annotations' in file {json_file_name}, check your label file"
            )
        if anno.get("image_id") is None:
            raise LabelException(
                f"There is not 'image_id' in 'annotations' in file {json_file_name}, check your label file"
            )
        if anno.get("bbox") is None:
            raise LabelException(
                f"There is not 'bbox' in 'annotations' in file {json_file_name}, check your label file"
            )
        if type(anno.get("category_id")) != int or anno.get("category_id") <= -1:
            raise LabelException(
                f"There is inappropriate 'category_id' value in {json_file_name}."
            )
        class_ids.append(anno.get("category_id"))
        for img in images:
            if img.get("id") == anno.get("image_id"):
                validate_coco_bbox(
                    anno.get("bbox"), img.get("width"), img.get("height")
                )
    if max(class_ids) != max_classes:
        raise LabelException(
            "Your label file has more categories information than expacted. Check 'annotations' in your label file."
        )


def get_num_classes(categories: Dict[List, Dict[str, int]]):
    num_classes = []
    for c in categories:
        if type(c["id"]) != int or c["id"] <= -1:
            raise LabelException(
                f"There is inappropriate 'category_id' value in your label file."
            )
        num_classes.append(c["id"])  # id start with '0'
    max_num_classes = max(num_classes)
    if len(categories) != (max_num_classes + 1):
        raise LabelException(
            "Your label file has more categories information than expacted. Check 'categories' in your label file."
        )
    return max_num_classes


def validate_label_files(label_list: List[str], num_classes: int):
    for ll in label_list:
        json_dict = json_load(ll)
        p = PurePath(ll)
        p = str(p.parts[-1])  # p == file name like '098.json'
        if not json_dict.get("images"):
            raise LabelException(f"There is not 'images' key in file {p}")
        # validate_coco_images_exist(json_dict.get('images')) -> maybe TODO
        if not json_dict.get("annotations"):
            raise LabelException(f"There is not 'annotations' key in file {p}")
        num_categories = []
        if not json_dict.get("categories"):
            raise LabelException(f"There is not 'categories' key in file {p}")
        categories = json_dict.get("categories")
        max_classes = get_num_classes(categories)
        if (max_classes + 1) != num_classes:
            raise LabelException(
                "Your label file has more categories information than expacted. Number of it not matched with num_classes."
            )
        images = json_dict["images"]
        annotations = json_dict["annotations"]
        validate_coco_label(images, annotations, p, max_classes)


def validate_json_exist(dir_path: Path):
    dirs = get_dir_list(dir_path)
    img_file_types = [
        "*.jpeg",
        "*.JPEG",
        "*.jpg",
        "*.JPG",
        "*.png",
        "*.PNG",
        "*.BMP",
        "*.bmp",
    ]
    image_dir_paths = get_target_dirs(dirs, img_file_types)
    json_dir_paths = get_target_dirs(dirs, ["*.json"])
    if len(image_dir_paths) != len(json_dir_paths):
        raise LabelException(".json file have to exist~~~")


def validate(root_path: str, num_classes: int, format:str, delete=False):
    dir_path = Path(root_path)
    dir_paths = validate_first_dirs(dir_path)
    validate_second_dirs(dir_paths)
    validate_dataset_type(root_path, format)
    img_list, label_list = get_file_lists(dir_paths)
    validate_json_exist(dir_path)
    validate_data_yaml(dir_path, num_classes)
    validate_label_files(label_list, num_classes)
    if delete:
        delete_dirs(dir_path)


if __name__ == "__main__":
    validate("devtest/zip2_coco", "zip2_coco", 3)
