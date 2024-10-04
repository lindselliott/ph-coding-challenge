# ph-coding-challenge
PH Coding Challenge

This is a python microservice that is able to 
- accept and store an uploaded DICOM file, extract
- return any DICOM header attribute based on a DICOM Tag as a query parameter
- finally convert the file into a PNG for browser-based viewing.


Please design a RESTful API that exposes an interface for the functionality described above.

Testing: Drop your DICOM file in the test_files folder


How to run:

In project directory:
`source myenv/bin/activate`

In virtual environment:
`python app.py`



http://127.0.0.1:5000/?tag=00041130
`(0004, 1130) File-set ID                         CS: 'DicomDir'` 

http://127.0.0.1:5000/?tag=00100010 
`(0010, 0010) Patient's Name                      PN: 'NAYYAR^HARSH'`

