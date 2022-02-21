import argparse
from src.utils import validate


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset validator.")
    parser.add_argument("--dir", type=str, required=True, help="dataset path.")
    parser.add_argument("--format", type=str, required=True, help="dataset format")
    parser.add_argument("--task", type=str, default="detection", help="task")
    parser.add_argument("--yaml_path", type=str, required=True, help="yaml file path")
    parser.add_argument("--fix", type=bool, default=False, help="use auto fix")
    args = parser.parse_args()
    dir_path, dataset_type, task, yaml_path, fix = (
        args.dir,
        args.format.lower(),
        args.task.lower(),
        args.yaml_path,
        args.fix,
    )
    validate(dir_path, dataset_type, yaml_path, task, fix=fix, local=True)