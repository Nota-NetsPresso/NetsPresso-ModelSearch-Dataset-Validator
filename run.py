import argparse
from src.utils import validate, structure_convert, zip_packing
import shutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset validator.")
    parser.add_argument("--dir", type=str, required=True, help="dataset path.")
    parser.add_argument("--format", type=str, required=True, help="dataset format")
    parser.add_argument("--task", type=str, default="detection", help="task")
    parser.add_argument("--yaml_path", type=str, required=True, help="yaml file path")
    parser.add_argument("--data_type", type=str, required=True, help="train / test / val")
    args = parser.parse_args()

    dir_path, dataset_type, task, yaml_path, data_type= (
        args.dir,
        args.format.lower(),
        args.task.lower(),
        args.yaml_path,
        args.data_type
    )

    tmp_path = structure_convert(dir_path)
    succeed = validate(tmp_path, dataset_type, yaml_path, task)
    if succeed:
        zip_packing(tmp_path, f"./{data_type}.zip")
        shutil.rmtree(tmp_path)
    else:
        shutil.rmtree(tmp_path)
