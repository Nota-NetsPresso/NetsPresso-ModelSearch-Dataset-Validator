# Validate your dataset structure to use NetsPresso
This repository can be used to validate dataset structure to use NetsPresso.

## How to use
Run the code sample below to validate if the data is ready-to-use. If you do not get any error message, you are all set! If error occurs, please refer to the error message to resolve the issue.
- dir_path: Root directory path of your dataset
- format: Format of your dataset
- num_classes: Number of classes in your dataset
```
# python3 run.py --dir {your_dataset_dir_path} --format {format_of_your_dataset} --num_classes {number_of_your_dataset_classes}
python3 run.py --dir datasets/yolo --format yolo --num_classes 80
```
#### Example of error message
```
netspresso@netspresso:~/dataset_validator$ PYTHONPATH=. python3 run.py --dir yolo --format yolo --num_classes 11
Traceback (most recent call last):
  File "run.py", line 13, in <module>
    validate(dir_path, num_classes)
  File "/hdd1/home/dataset_validator/src/yolo.py", line 49, in validate
    validate_image_files_exist(img_list, label_list, "txt")
  File "/hdd1/home/dataset_validator/src/utils.py", line 186, in validate_image_files_exist
    f"There is no image file for label file '{label_name}.{suffix}'"
src.exceptions.ImageException: There is no image file for label file 'yolo/train/labels/000000000025.txt'
```

## Dataset structure for NetsPresso
NetsPresso supports YOLO, COCO, and VOC formats for object detection tasks. (YOLO format is recommended.)
There are labeling tools, such as [CVAT][cvatlink] and [labelimg][labelimglink] support these annotation formats.

### Prepare dataset yaml file
Regardless of the dataset format, "data.yaml" file containing information about the class name and number of classes is needed.
- names: Names of classes
- nc: Number of classes

#### Yaml file example
```
names:
- fish
- jellyfish
- penguin
- puffin
- shark
- starfish
- stingray
nc: 7
```

### [YOLO] Dataset structure example
YOLO format has one '.txt' file per image with the same file name. If there is no object in the image file, no '.txt' file is required for the image. Make sure that every '.txt' file requires a corresponding image file.

For training, a "train" directory and at least one of "val" and "test" directories must exist in the dataset. A nested directory under images or labels is also allowed.

A sample zip file "example_datasets/yolo.zip" is in this repository.
```
{Your dataset dir}
├── train
│   ├── images
│   │   ├── {images or directories}
│   │   ├── example_1.jpg
│   │   └── example_2.jpg
│   │   └── sub_dir
│   │       ├── example_1.jpg
│   │       └── example_2.jpg
│   └── labels
│       ├── {labels same structure as images}
│       ├── example_1.txt
│       └── example_2.txt
│       └── sub_dir
│           ├── example_1.txt
│           └── example_2.txt
├── val
│   ├── images
│   │   └── {images or directories}
│   └── labels
│       └── {labels same structure as images}
├── test
│   ├── images
│   │   └── {images or directories}
│   └── labels
│       └── {labels same structure as images}
│
└── data.yaml
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

For training, a "train" directory and at least one of "val" and "test" directories must exist in the dataset. A nested directory under images or labels is also allowed.

A sample zip file "example_datasets/coco.zip" is in this repository.
```
{Your dataset dir}
├── train
│   ├── images
│   │   ├── {images or directories}
│   │   ├── example_1.jpg
│   │   ├── example_2.jpg
│   │   └── sub_dir
│   │       ├── example_1.jpg
│   │       └── example_2.jpg
│   └── labels
│       ├── {labels same structure as images}
│       ├── example.json (contain annotaion of images in "train/images/")
│       └── sub_dir
│           └── example.json (contain annotaion of images in "train/images/sub_dir/")
├── val
│   ├── images
│   │   └── {images or directories}
│   └── labels
│       └── {labels same structure as images}
├── test
│   ├── images
│   │   └── {images or directories}
│   └── labels
│       └── {labels same structure as images}
│
└── data.yaml
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

For training, all "train", "val", "test" directories must exist in the dataset. A nested directory under images or labels is also allowed.

A sample zip file "example_datasets/voc.zip" is in this repository.
```
{Your dataset dir}
├── train
│   ├── images
│   │   ├── {images or directories}
│   │   ├── example_1.jpg
│   │   └── example_2.jpg
│   │   └── sub_dir
│   │       ├── example_1.jpg
│   │       └── example_2.jpg
│   └── labels
│       ├── {labels same structure as images}
│       ├── example_1.xml
│       └── example_2.xml
│       └── sub_dir
│           ├── example_1.xml
│           └── example_2.xml
├── val
│   ├── images
│   │   └── {images or directories}
│   └── labels
│       └── {labels same structure as images}
├── test
│   ├── images
│   │   └── {images or directories}
│   └── labels
│       └── {labels same structure as images}
│
└── data.yaml
```

## Make .zip file with dataset
After validate data, make the '.zip' file like below.

#### Windows
![windows](https://user-images.githubusercontent.com/45225793/141430930-361439f0-5bb6-48ec-a86b-149c6a182527.gif)

#### Mac and Linux
```
zip -r {Dataset zip file name}.zip {Dataset diretory path} -x ".*" -x "__MACOSX"
```
![mac](https://user-images.githubusercontent.com/45225793/141430922-9a765546-1cea-4c6f-b6e2-ad391b49c735.gif)

Compare your '.zip' file with the images below.

#### Correct case

<p align="center"><img src="https://user-images.githubusercontent.com/69490987/141053041-18a2b5f3-c6c0-4a8a-8785-1a4bc20bcecc.png"></p>

#### Wrong case
<p align="center"><img src="https://user-images.githubusercontent.com/45225793/142646291-9121cac2-c905-494a-8ad5-f2756326612b.png"></p>




[cocoformat]: https://cocodataset.org/#format-data
[labelimglink]: https://github.com/tzutalin/labelImg
[cvatlink]: https://github.com/openvinotoolkit/cvat
[convert2yololink]: https://github.com/ssaru/convert2Yolo
[vocformat]: http://host.robots.ox.ac.uk/pascal/VOC/voc2007/
