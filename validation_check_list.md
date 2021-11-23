# Validation Check List
We consider zero is a positive number in this document.

## Common case

### Wrong directory structure
1. Any other directory than ['train', 'val', 'test'] is not accepted in first depth.
2. 'train' directory is in first depth.
3. 'val' or 'test' directory must be in first depth.
4. 'images' and 'labels' directory are in second depth.

### Dataset type
1. Dataset type is same with value of '--format'.

### data.yaml
1. 'data.yaml' is in first depth.
2. 'data.yaml' has 'names' and 'nc'.
3. Length of 'names', value of 'nc' and '--num_classes' are same.

## YOLO case
1. Image file is exsist if there is corresponding annotation file.
2. Each class number in annotation file is int.
3. Each class number in annotation file is positive value.
4. Each class number in annotation file is less than value of '--num_classes'.
5. Each coordinate in annotation file is positive.
6. Each line in annotation file have 5 numbers.
7. Each 'center_x' and 'center_y' in annotation file are equal or greater than 0.
8. Each 'center_x' and 'center_y' in annotation file are less than 1.
9. Each 'height' and 'width' in annotation file are equal or less than 1.
10. Each 'height' and 'width' in annotation file are greater than 0.

## COCO case
1. Image file is exsist if there is corresponding annotation information.
2. The label directory corresponding to the directory in which the image file is located must have the annotation file.
3. The key 'images' is exist in each annotation file.
4. The key 'categories' is exist in each annotation file.
5. The key 'annotations' is exist in each annotation file.

6. Lenght of 'categories' in each annotation file is same with value of '--num_classes'.
7. 'id' is exist for each elements of 'categories'.
8. Each 'id' in 'categories' is positive and int.
9. Each 'id' in 'categories' is less than value of '--num_classes'.

10. 'id' is exist for each elements of 'images'.
11. Each 'id' in 'images' is positive and int.
12. 'file_name' is exist for each elements of 'images'.
13. 'width' is exist for each elements of 'images'.
14. 'height' is exist for each elements of 'images'.

15. 'id' is exist for each elements of 'annotations'.
16. Each 'id' in 'annotations' is positive and int.
17. 'image_id' is exist for each elements of 'annotations'.
18. 'bbox' is exist for each elements of 'annotations'.
19. 'category_id' is exist for each elements of 'annotations'.
20. Each 'category_id' in 'annotations' is positive and int.

21. Each coordinate in 'bbox' is positive value.
22. Each 'x', 'y' coordinate value in 'bbox' are equal or greater than 0.
23. Each 'width', 'height' coordinate value in 'bbox' are greater than 0.
24. Each sum of 'x' and 'width' in 'bbox' is equal or less than corresponding image width.
25. Each sum of 'y' and 'height' in 'bbox' is equal or less than corresponding image height.

## VOC case
1. Image file is exsist if there is corresponding annotation file.
2. 'names' in 'data.yaml' have to match with 'name' tag value in annotation files.
* For example, when class name in xml annotation file is 'diningtable'. if 'dining table' in 'names' in 'data.yaml' is wrong case.
3. Each coordinate in annotation file is positive.
4. Each 'xmin' and 'ymin' in annotation file are equal or greater than 0.
5. Each 'xmax' in annotation file is greater than 'xmin'.
6. Each 'xmax' in annotation file is less than value of 'width' tag.
7. Each 'ymax' in annotation file is greater than 'ymin'.
8. Each 'ymax' in annotation file is less than value of 'height' tag.
9. The 'filename' element value of the XML file should have the image file name corresponding to the label information.
