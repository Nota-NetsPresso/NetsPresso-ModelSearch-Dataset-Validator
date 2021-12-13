import argparse
import importlib
from src.utils import validate


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Dataset validator.')
    parser.add_argument('--dir', type=str, required=True, help='dataset path.')
    parser.add_argument('--format', type=str, required=True, help='dataset format')
    parser.add_argument('--yaml_path', type=str, required=True, help='yaml file path')
    args = parser.parse_args()
    dir_path, dataset_type, yaml_path = args.dir, args.format.lower(), args.yaml_path
    validate(dir_path, dataset_type, yaml_path, online=False)