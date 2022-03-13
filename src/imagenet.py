from typing import Dict, List
from pathlib import Path
from src.utils import get_img_file_types, log_n_print


def validate_img_file_type(
    dir_paths: List[str], 
    errors: List[str],
):
    img_file_types = get_img_file_types()
    for path in dir_paths:
        files  = Path(path).glob("**/*")
        for f in files:
            if f.is_file() and ('*'+f.suffix) not in img_file_types:
                errors.append(f"{f} is not supported image file type")
    return errors

def validate_classes(
    dir_paths: List[str], 
    label_list: List[str], 
    errors: List[str],
):
    for path in dir_paths:
        if sorted(label_list) != get_classes(path):
            errors.append(f"Classes of yaml file and {path} does not match")
    return errors

def get_classes(target_path: str):
    class_list = []
    for p in Path(target_path).glob("*"):
        if p.is_dir():
            class_list.append(str(p.name))
    return sorted(class_list)

def validate(
    label_list: List[str], 
    dir_paths: List[str], 
    errors: List[str],
):
    errors = validate_classes(dir_paths, label_list, errors)
    log_n_print("[Validate: 2/3]: Validation finished for matching classes of yaml file and image folders.")
    errors = validate_img_file_type(dir_paths, errors)
    log_n_print("[Validate: 3/3]: Validation finished for image file types.")

    return errors
