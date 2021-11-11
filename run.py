import argparse
import importlib


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Dataset validator.')
    parser.add_argument('--dir', type=str, required=True, help='dataset path.')
    parser.add_argument('--num_classes', type=int, required=True, help='# of classes')
    parser.add_argument('--format', type=str, required=True, help='dataset format')
    args = parser.parse_args()
    dir_path, num_classes, dataset_type = args.dir, args.num_classes, args.format
    validate = getattr(importlib.import_module(f"src.{dataset_type}"), "validate")
    validate(dir_path, num_classes)