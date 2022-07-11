import argparse
from src.utils import validate, structure_convert, zip_packing, make_yaml_file, calc_file_hash,  get_object_stat, yolo_stat
import shutil
import os
import yaml

def main(dir_path, format, task, data_type, yaml_path=None):
    if format == "yolo" and yaml_path is None:
        raise Exception("yaml_path should be defined for yolo format ")

    if format in ["coco", "voc"]:
        tmp_path, names, obj_stat, num_images = structure_convert(dir_path, format)
        yaml_path = f"./{data_type}_data.yaml"
        make_yaml_file(names, yaml_path, num_images, obj_stat)
    else:
        
        tmp_path = dir_path
        names, obj_stat, num_images = yolo_stat(tmp_path, yaml_path)
        new_yaml_path = f"./{data_type}_data.yaml"
        make_yaml_file(names, new_yaml_path, num_images, obj_stat)




    succeed = validate(tmp_path, format, yaml_path, task)
    zip_file_path = f"./{data_type}.zip"
    
    if succeed:
        zip_packing(tmp_path, zip_file_path)
        with open("./validation_key.np", 'w') as f:
            f.write(calc_file_hash(zip_file_path))
        if format in ["coco", "voc"]:
          shutil.rmtree(tmp_path)
    else:
        if format in ["coco", "voc"]:
          shutil.rmtree(tmp_path)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset validator.")
    parser.add_argument("--dir", type=str, required=True, help="dataset path.")
    parser.add_argument("--format", type=str, required=True, help="dataset format")
    parser.add_argument("--task", type=str, default="detection", help="task")
    parser.add_argument("--yaml_path", type=str, required=False, help="yaml file path")
    parser.add_argument("--data_type", type=str, required=True, help="train / test / val")
    args = parser.parse_args()

    dir_path, format, task, yaml_path, data_type= (
        args.dir,
        args.format.lower(),
        args.task.lower(),
        args.yaml_path,
        args.data_type
    )

    main(dir_path, format, task, data_type, yaml_path)