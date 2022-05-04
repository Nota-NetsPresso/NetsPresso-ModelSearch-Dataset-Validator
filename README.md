# Validate your dataset structure to use NetsPresso
This repository can be used to validate dataset structure to use NetsPresso.

## How to use

#### Install requirements
```
pip3 install -r requirements.txt
```
#### Run
Run the code sample below to validate if the data is ready-to-use. If you do not get any error message, you are all set! If error occurs, please refer to the error message to resolve the issue.

- dir_path: Root directory path of dataset.
- format: Format of dataset.
- yaml_path: Yaml file path with data set information. More information about yaml file is in [Prepare dataset yaml file][yaml_file]
```
# PYTHONPATH=. python3 run.py --dir {dataset_dir_path} --format {format_of_dataset} --yaml_path {yaml_file_path}
PYTHONPATH=. python3 run.py --dir datasets/yolo/train --format yolo --yaml_path datasets/data.yaml
```
### Example of error message

#### Validation success case
```
netspresso@netspresso:~/NetsPresso-ModelSearch-Dataset-Validator$ PYTHONPATH=. python3 run.py --dir yolo/train --format yolo --yaml_path data.yaml
Start dataset validation.
[Validate: 1/5]: Done validation dir structure ['images', 'labels'].
[Validate: 2/5]: Done validation, user select correct data type.
[Validate: 3/5]: Done validation for data.yaml file.
[Validate: 4/5]: Validation finished for existing image files in the correct position.
[Validate: 5/5]: Validation finished for label files.
Validation completed! Now try your dataset on NetsPresso!
```

#### Validation fail case
For more detail, please see [Validation check list][validationchecklist]

In case of validation fail with traceback, please read exception error message.
```
netspresso@netspresso:~/NetsPresso-ModelSearch-Dataset-Validator$ PYTHONPATH=. python3 run.py --dir yolo/train --format yolo --yaml_path data.yaml
Start dataset validation.
[Validate: 1/5]: Done validation dir structure ['images', 'labels'].
[Validate: 2/5]: Done validation, user select correct data type.
[Validate: 3/5]: Done validation for data.yaml file.
Traceback (most recent call last):
  File "run.py", line 13, in <module>
    validate(dir_path, num_classes, dataset_type)
  File "/hdd1/home/NetsPresso-ModelSearch-Dataset-Validator/src/utils.py", line 307, in validate
    yaml_label, errors = validate_data_yaml(dir_path, num_classes, errors)
  File "/hdd1/home/NetsPresso-ModelSearch-Dataset-Validator/src/utils.py", line 199, in validate_data_yaml
    raise YamlException("There is no 'names' in data.yaml.")
src.exceptions.YamlException: There is no 'names' in data.yaml.
```
In case of validation fail with **Validation error, please check 'validation_result.txt'.**, please check validation_result.txt file to resolve failure.
```
netspresso@netspresso:~/NetsPresso-ModelSearch-Dataset-Validator$ PYTHONPATH=. python3 run.py --dir yolo/train --format yolo --yaml_path data.yaml
Start dataset validation.
[Validate: 1/5]: Done validation dir structure ['images', 'labels'].
[Validate: 2/5]: Done validation, user select correct data type.
[Validate: 3/5]: Done validation for data.yaml file.
[Validate: 4/5]: Validation finished for existing image files in the correct position.
[Validate: 5/5]: Validation finished for label files.
Validation error, please check 'validation_result.txt'.
```
And contents of 'validation_result.txt are like below.
```
There is no image file for annotation file 'yolo/train/labels/000000000025.txt'
There is no image file for annotation file 'yolo/test/labels/000000000337.txt'
```

#### Validation autofix for yolo format.
In the case of yolo format, when the valuation fails, the dataset can be partially modified using the autofix. Autofix is to delete the row if there is an inappropriate value in the annotation file. When executing run.py, it can be executed by adding ‘--fix’ config as true. 
```
PYTHONPATH=. python3 run.py --fix true --dir datasets/yolo/train --format yolo --yaml_path datasets/data.yaml
```

## Dataset structure for NetsPresso
NetsPresso supports YOLO, COCO, and VOC formats for object detection tasks. (YOLO format is recommended.)
There are labeling tools, such as [CVAT][cvatlink] and [labelimg][labelimglink] support these annotation formats.

## Supported image file types
'bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo' are supported.

### Prepare dataset yaml file
Regardless of the dataset format, "data.yaml" file containing information about the class name and number of classes is needed.
- For the coco data form, all elements of the names must be written in the same number order as category_id of the dataset.
- For the voc data form, all elements of the names must be written alphabetically.
- For the yolo data form, all elements of the names must be written in the same class number as the dataset.
- names: Names of classes
- nc: Number of classes

#### Yaml file example
```
names:
- aeroplane
- bicycle
- bird
- boat
- bottle
- bus
- car
- cat
- chair
- cow
- diningtable
- dog
- horse
- motorbike
- person
- pottedplant
- sheep
- sofa
- train
- tvmonitor
nc: 20
```

### [YOLO] Dataset structure example
YOLO format has one '.txt' file per image with the same file name. If there is no object in the image file, no '.txt' file is required for the image. Make sure that every '.txt' file requires a corresponding image file.
To train a model, a "train" dataset and at least one of "val" and "test" dataset must exist and uploaded.
A nested directory under images or labels is also allowed.
A sample zip files are in this repository "example_datasets/".
```
{root_dir}
   ├── images
   │   ├── {images or directories}
   │   ├── example_1.jpg
   │   └── example_2.jpg
   └── labels
       ├── {labels same structure as images}
       ├── example_1.txt
       └── example_2.txt
```

### Dataset file example for YOLO format
![sample](https://user-images.githubusercontent.com/45225793/141430419-9c94f0ba-d08f-4d73-83c1-78947cbdae84.png)
<p align="center"><img src="https://user-images.githubusercontent.com/45225793/128144814-3f613edf-3a31-4d88-878d-45ac01ca08a3.png"></p>

- One row per object
- Each row is ```{class number} {center_x} {center_y} {width} {height}```
- Box coordinates must be in normalized xywh format (from 0 - 1). If your boxes are in pixels, divide ```center_x``` and ```width``` by image width, and ```center_y``` and ```height``` by image height.
  - For example,  an image above has a size of ```width 623px, height 396px```. And the coordinate of first object in its label are ```center_x 259, center_y 196, width 246, height 328```. After normalization, the coordinates are ```center_x 0.415730, center_y 0.494949, width 0.394864, height 0.828283```.
- Class numbers are zero-indexed (starting from 0).

### [COCO] Dataset structure example
Please refer to the official [COCO Data format][cocoformat] for COCO label format.

COCO format has all images in {images} folder and a single '.json' file with annotations in {labels} folder. If you split data into multiple sets, each set should have its own directory and a '.json' file.
To train a model, a "train" dataset and at least one of "val" and "test" dataset must exist and uploaded.
A nested directory under images or labels is also allowed.
A sample zip files are in this repository "example_datasets/".
```
{root_dir}
   ├── images
   │   ├── {images or directories}
   │   ├── example_1.jpg
   │   └── example_2.jpg
   └── labels
       ├── {labels same structure as images}
       └── example.json (contain annotaion of images in "train/images/")
```

If supercategory is in the ".json" file, it have to be written in "data.yaml" file too. Please see example below.

```
    "categories": [
        {
            "id": 0,
            "name": "animal",
            "supercategory": "none"
        },
        {                                        names:
            "id": 1,                             - animal
            "name": "cat",                =>     - cat
            "supercategory": "animal"            - dog
        },                                       nc: 3
        {
            "id": 2,
            "name": "doc",
            "supercategory": "animal"
        }
    ]
```

### [VOC] Dataset structure example
VOC format has one '.xml' file per image with the same file name. If there is no object in an image, no '.xml' file is required for the image. Make sure that every '.txt' file requires a corresponding image file.
Please refer to the official [VOC Data format][vocformat] for VOC label format.
To train a model, a "train" dataset and at least one of "val" and "test" dataset must exist and uploaded.
A nested directory under images or labels is also allowed.
A sample zip files are in this repository "example_datasets/".
```
{root_dir}
   ├── images
   │   ├── {images or directories}
   │   ├── example_1.jpg
   │   └── example_2.jpg
   └── labels
       ├── {labels same structure as images}
       ├── example_1.xml
       └── example_2.xml
```

## Make .zip file with dataset
After validate data, make the '.zip' file like below.

#### Windows
![windows](https://user-images.githubusercontent.com/69490987/162886468-db1ca951-9770-4c42-a37f-61f452c1b957.gif)


#### Mac and Linux
```
zip -r {Dataset zip file name}.zip {Dataset diretory path} -x ".*" -x "__MACOSX"
```
![Dec-23-2021 16-45-20](https://user-images.githubusercontent.com/69490987/162886518-e6becf1b-14af-4cf5-a9f1-510c4f516003.gif)


Compare your '.zip' file with the images below.

#### Correct case

<img src="https://user-images.githubusercontent.com/69490987/162886538-71ac03ac-b82b-4fa3-8065-948e31356bf2.png">

#### Wrong case
![101db6f-wrong_case](https://user-images.githubusercontent.com/69490987/162886544-4160d1bb-a25a-4131-af07-8c63fc676d5f.png)


[cocoformat]: https://cocodataset.org/#format-data
[labelimglink]: https://github.com/tzutalin/labelImg
[cvatlink]: https://github.com/openvinotoolkit/cvat
[convert2yololink]: https://github.com/ssaru/convert2Yolo
[vocformat]: http://host.robots.ox.ac.uk/pascal/VOC/voc2007/
[validationchecklist]: https://github.com/Nota-NetsPresso/NetsPresso-ModelSearch-Dataset-Validator/blob/main/validation_check_list.md
[yaml_file]:https://github.com/Nota-NetsPresso/NetsPresso-ModelSearch-Dataset-Validator/tree/main#yaml-file-example
