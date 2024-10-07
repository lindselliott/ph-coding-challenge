# ph-coding-challenge
PH Coding Challenge

This is a python microservice that is able to 
- accept and store an uploaded DICOM file, extract
- return any DICOM header attribute based on a DICOM Tag as a query parameter
- convert the file into a PNG.



## How to run:

In project directory need to get into environment:

```
source myenv/bin/activate
```

Run app in virtual environment:
```
python app.py
```

## Endpoints: 
---

#### Upload file
Use the endpoint to upload a DCM file, it will appear in the `/uploads` folder on success. 

`POST` http://127.0.0.1:5000/upload 

BODY:  
File to upload 
![Example](<Screenshot 2024-10-07 at 12.31.04 PM.png>)

Example Output:
```
File IM000001 uploaded successfully
```

---

#### Get Tag

Use this enpoint to get the value of a tag given a DCM file already uploaded using the filename. Output is a json of the tag. 

`GET` http://127.0.0.1:5000/tag?tag=0X00100010&file_name=IM000001

Query params: 
- `tag` - required
- `file_name` - required

Example Output:
```
{"Value": [{"Alphabetic": "NAYYAR^HARSH"}], "vr": "PN"}
```

---
#### Get Image

Use this enpoint to generate a PNG from a DCM file using the filename (existing in `uploads` folder). This png file will be saved in the `/export` directory. 

`GET` http://127.0.0.1:5000/image?file_name=IM000001 

Query params: 
- `file_name` - required

Example Output: 
```
File IM000001 saved as png to export folder
```

---

### Testing

##### Examples of nested tags.

http://127.0.0.1:5000/tag?tag=00080060&file_name=IM000001

`(0004, 1130) File-set ID                         CS: 'DicomDir'` 

Output as JSON:

```
{"Value": ["DicomDir"], "vr": "CS"}
```


Tag in A Sequence Data Element:

http://127.0.0.1:5000/tag?tag=00100010&file_name=IM000001

`(0010, 0010) Patient's Name                      PN: 'NAYYAR^HARSH'`

Output as JSON:

```
{"Value": [{"Alphabetic": "NAYYAR^HARSH"}], "vr": "PN"}
```


Tag Not Found:

http://127.0.0.1:5000/tag?tag=00080061&file_name=IM000001

```
Tag not found in DICOM file: 00080061
```

---
