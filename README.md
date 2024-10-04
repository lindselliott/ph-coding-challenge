# ph-coding-challenge
PH Coding Challenge

This is a python microservice that is able to 
- accept and store an uploaded DICOM file, extract
- return any DICOM header attribute based on a DICOM Tag as a query parameter
- finally convert the file into a PNG for browser-based viewing.



## How to run:

In project directory:

```
source myenv/bin/activate
```


Testing: 

Drop your DICOM file in the `test_files`` folder

line 41 of `app.py`

`path = "test_files/XRAY/DICOMDIR"`


In virtual environment:
```
python app.py
```

### Example endpoints: 

Tag in First Layer of DICOM File:

http://127.0.0.1:5000/?tag=00041130

`(0004, 1130) File-set ID                         CS: 'DicomDir'` 

Output as JSON:

```
{"Value": ["DicomDir"], "vr": "CS"}
```


Tag in A Sequence Data Element:

http://127.0.0.1:5000/?tag=00100010 

`(0010, 0010) Patient's Name                      PN: 'NAYYAR^HARSH'`

Output as JSON:

```
{"Value": [{"Alphabetic": "NAYYAR^HARSH"}], "vr": "PN"}
```


Tag Not Found:

http://127.0.0.1:5000/?tag=00080061 

```
Tag not found in DICOM file: 00080061
```
