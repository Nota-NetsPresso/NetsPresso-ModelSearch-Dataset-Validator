import argparse
import importlib
from src.utils import validate


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Dataset validator.')
    parser.add_argument('--dir', type=str, required=True, help='dataset path.')
    parser.add_argument('--format', type=str, required=True, help='dataset format')
    args = parser.parse_args()
    dir_path, dataset_type = args.dir, args.format
    validate(dir_path, dataset_type)