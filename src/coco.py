import glob
import os
import shutil
import sys
import zipfile
from pathlib import Path, PurePath, PurePosixPath
from typing import Dict, List

import yaml

from src.utils import (get_file_lists, validate_first_dirs,
                       json_load, validate_data_yaml,
                       validate_dataset_type, validate_first_dirs,
                       validate_second_dirs, get_dir_list,
                       get_img_file_types, get_target_dirs)


def validate_coco_bbox(
    bbox: List[float], 
    width: float, 
    height: float, 
    label_file: str,
    annotation_id: int,
    errors:List[str]
):
    x, y, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
    if not width >= x + w:
        errors.append(
            f"'x'+'width' in bbox cannot be greater than Image file's width, please check annotations['id'] = {annotation_id} in {label_file}."
        )
    if not height >= y + h:
        errors.append(
            f"'y'+'height' in bbox cannot be greater than Image file's width, please check annotations['id'] = {annotation_id} in {label_file}."
        )
    if not x >= 0:
        errors.append(
            f"'x' in bbox cannot be a negative value, please check annotations['id'] = {annotation_id} in {label_file}."
        )
    if not y >= 0:
        errors.append(
            f"'y' in bbox cannot be a negative value, please check annotations['id'] = {annotation_id} in {label_file}."
        )
    if not w > 0:
        errors.append(
            f"'width' in bbox cannot be a negative value, please check annotations['id'] = {annotation_id} in {label_file}."
        )
    if not h > 0:
        errors.append(
            f"'height' in bbox cannot be a negative value, please check annotations['id'] = {annotation_id} in {label_file}."
        )
    if not width >= x:
        errors.append(
            f"'width' in bbox cannot be less than 'x', please check annotations['id'] = {annotation_id} in {label_file}."
        )
    if not height >= y:
        errors.append(
            f"'height' in bbox cannot be less than 'y', please check annotations['id'] = {annotation_id} in {label_file}."
        )
    return errors


def validate_coco_label(
    images: List[Dict], 
    annotations: List[Dict], 
    json_file_name: str, 
    num_classes: int,
    errors: List[str]
):
    class_ids = []
    for img in images:
        if img.get("id") is None:
            errors.append(
                f"There is an image information without 'id' in 'images' in file {json_file_name}."
            )
        if img.get("file_name") is None:
            errors.append(
                f"There is an image information without 'file_name' in 'images' where id is {img.get('id')} in file {json_file_name}."
            )
        if img.get("height") is None:
            errors.append(
                f"There is an image information without 'height' in 'images' where id is {img.get('id')} in file {json_file_name}."
            )
        if img.get("width") is None:
            errors.append(
                f"There is an image information without 'width' in 'images' where id is {img.get('id')} in file {json_file_name}."
            )
    for anno in annotations:
        if anno.get("id") is None:
            errors.append(
                f"There is an annotation information without 'id' in 'annotations' in file {json_file_name}."
            )
        if anno.get("image_id") is None:
            errors.append(
                f"There is an annotation information without 'image_id' in 'annotations' where id is {anno.get('id')} in file {json_file_name}."
            )
        if anno.get("bbox") is None:
            errors.append(
                f"There is an annotation information without 'bbox' in 'annotations'  where id is {anno.get('id')} in file {json_file_name}."
            )
        if type(anno.get("category_id")) != int or anno.get("category_id") <= -1:
            errors.append(
                f"There is an inappropriate 'category_id' value in {json_file_name}."
            )
        else:
            class_ids.append(anno.get("category_id"))
        for img in images:
            if (img.get("id") == anno.get("image_id")) and anno.get("bbox") and img.get("width") and img.get("height"):
                errors = validate_coco_bbox(
                    anno.get("bbox"), 
                    img.get("width"), 
                    img.get("height"), 
                    json_file_name, 
                    anno.get("id"), 
                    errors)
    if max(class_ids) > num_classes-1:
        errors.append(
            f"'category_id' value {max(class_ids)} is greater than expected. Check 'annotations' in {json_file_name}.'category_id' have to be equal or less than {num_classes-1}."
        )
    return errors

def validate_category_id(categories: Dict[List, Dict[str, int]], json_path:str, errors:List[str]):
    num_classes = []
    for c in categories:
        if c.get("id") is None:
            errors.append(
                f"There is a category information without 'id' in 'categories' in {json_path}."
            )
        elif type(c["id"]) != int or c["id"] <= -1:
            errors.append(
                f"There is an inappropriate 'id' value {c['id']} in 'categories' in {json_path}."
            )
    return max_num_classes, errors


def validate_label_files(label_list: List[str], num_classes: int, errors:List[str]):
    for ll in label_list:
        json_dict = json_load(ll)
        if not json_dict.get("images"):
            errors.append(f"'images' key does not exist in the file {ll}.")
        # validate_coco_images_exist(json_dict.get('images')) -> maybe TODO
        if not json_dict.get("annotations"):
            errors.append(f"'annotations' key does not exist in the file {ll}.")
        num_categories = []
        if not json_dict.get("categories"):
            errors.append(f"'categories' key does not exist in the file {ll}.")
        categories = json_dict.get("categories")
        errors = validate_category_id(categories, ll, errors)
        images = json_dict["images"]
        annotations = json_dict["annotations"]
        errors = validate_coco_label(images, annotations, ll, num_classes, errors)
    return errors


def validate_json_exist(dir_path: Path, errors:List[str]):
    dirs = get_dir_list(dir_path)
    img_file_types = get_img_file_types()
    image_dir_paths = get_target_dirs(dirs, img_file_types)
    json_dir_paths = get_target_dirs(dirs, ["*.json"])
    if len(image_dir_paths) != len(json_dir_paths):
        errors.append("'json' annotation file must exist in the corresponding directory. Please read 'https://github.com/Nota-NetsPresso/NetsPresso-ModelSearch-Dataset-Validator#coco-dataset-structure-example'")
    return errors


def validate(
    dir_path: str, 
    num_classes: int, 
    label_list:List[str], 
    img_list:None,
    yaml_label:None,
    errors:List[str]):
    """
    'img_list' and 'yaml_label' are not used in this function, but written for dynamic importing in src.utils.py
    """
    errors = validate_json_exist(dir_path, errors)
    print("[Validate: 5/6]:  Validation finished for existing json files in the correct position.")
    errors = validate_label_files(label_list, num_classes, errors)
    print("[Validate: 6/6]: Validation finished for label files.")
    return errors
