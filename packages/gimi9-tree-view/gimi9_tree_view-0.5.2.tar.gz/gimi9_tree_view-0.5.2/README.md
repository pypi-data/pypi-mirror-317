linux tree utility의 개선.

bigdata 분석 및 문서화에 활용하기 좋은 기능을 포함.

Python 3.12.3 기준으로 작성되었으며, Python 3.10 이상에서 동작합니다. 아마도 3.2 이상이면 다 동작할 것으로 예상됩니다.
 

## 기능

* tree 구조 출력
* size: human readable
* file count
* file list limit
* 📂 emoji

treeview -h
```
usage: Main.py [-h] [-d] [-L LEVEL] [-n MAX_FILES] directory

List directory contents.

positional arguments:
  directory             Directory to read

options:
  -h, --help            show this help message and exit
  -d                    List directories only
  -L LEVEL, --level LEVEL
                        Descend only level directories deep
  -n MAX_FILES, --max-files MAX_FILES
                        Print only N files in each directory
```

## 출력 예

treeview 3d_car_instance_sample
```
📂 3d_car_instance_sample [2 GB]
└──📂 3d_car_instance_sample [2 GB]
    ├──📂 camera [340 B    2 개의 파일]
    │   ├── 5.cam [169 B]
    │   └── 6.cam [171 B]
    ├──📂 car_models [25 MB    79 개의 파일]
    │   ├── 019-SUV.pkl [338 KB]
    │   ├── 036-CAR01.pkl [329 KB]
    │   ├── 037-CAR02.pkl [354 KB]
    │   └── MG-GT-2015.pkl [313 KB]
    ├──📂 car_poses [1 MB    1,003 개의 파일]
    │   ├── 180116_053947113_Camera_5.json [1 KB]
    │   ├── 180116_053947909_Camera_5.json [2 KB]
    │   ├── 180116_053948523_Camera_5.json [2 KB]
    │   └── 180116_053949115_Camera_5.json [1 KB]
    ├──📂 images [2 GB    1,003 개의 파일]
    │   ├── 180116_053947113_Camera_5.jpg [2 MB]
    │   ├── 180116_053947909_Camera_5.jpg [2 MB]
    │   ├── 180116_053948523_Camera_5.jpg [2 MB]
    │   └── 180116_053949115_Camera_5.jpg [2 MB]
    └──📂 split [29 KB    2 개의 파일]
       ├── train.txt [21 KB]
       └── val.txt [8 KB]
```

treeview -d 3d_car_instance_sample
```
📂 3d_car_instance_sample [2 GB]
└──📂 3d_car_instance_sample [2 GB]
    ├──📂 camera [340 B    2 개의 파일]
    ├──📂 car_models [25 MB    79 개의 파일]
    ├──📂 car_poses [1 MB    1,003 개의 파일]
    ├──📂 images [2 GB    1,003 개의 파일]
    └──📂 split [29 KB    2 개의 파일]
```

reeview -d -L 1 3d_car_instance_sample
```
📂 3d_car_instance_sample [2 GB]
└──📂 3d_car_instance_sample [2 GB]
```

treeview -n 1 3d_car_instance_sample
```
📂 3d_car_instance_sample [2 GB]
└──📂 3d_car_instance_sample [2 GB]
    ├──📂 camera [340 B    2 개의 파일]
    │   └── 5.cam [169 B]
    ├──📂 car_models [25 MB    79 개의 파일]
    │   └── 019-SUV.pkl [338 KB]
    ├──📂 car_poses [1 MB    1,003 개의 파일]
    │   └── 180116_053947113_Camera_5.json [1 KB]
    ├──📂 images [2 GB    1,003 개의 파일]
    │   └── 180116_053947113_Camera_5.jpg [2 MB]
    └──📂 split [29 KB    2 개의 파일]
       └── train.txt [21 KB]
```
