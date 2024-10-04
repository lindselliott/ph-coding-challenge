from flask import Flask, request, jsonify
import pydicom
from pydicom.data import get_testdata_file
from pydicom.fileset import FileSet
import os

app = Flask(__name__)

# Global variable to store the DICOM data
dicom_data = None

def find_tag(tag, ds, indent=""):
    # Check if the tag is in the dataset and print the result
    if tag in ds:
        value = ds.get(tag)
        return value

    # Loop through all elements in the dataset
    for elem in ds:
        # If the element is a sequence (VR == "SQ"), recurse on each item in the sequence
        if elem.VR == "SQ":
            #print(indent + f"Checking sequence: {elem}")
            for item in elem:
                # Recursively call find_tag and capture its return value
                result = find_tag(tag, item, indent + "    ")
                # If a result is found, return it
                if result != -1:
                    return result
    return -1

@app.route('/')
def home():
    # Path to DICOM file
    path = "test_files/XRAY/DICOMDIR"

    # Get the DICOM tag requested in the query parameter 'tag'
    tag = request.args.get('tag')

    # A File-set can be loaded from the path to its DICOMDIR dataset
    dicom_data = pydicom.dcmread(path)
    print (dicom_data)

    try:
        # Try to convert the tag into an integer (DICOM tags are integers)
        tag_int = int(tag, 16)  # Tags are often in hexadecimal
        value = find_tag(tag_int, dicom_data, indent="")
        print(value)        

    except Exception as e:
                return f"Error reading DICOM file: {e}", 400
   
    return "Hello, Flask!"


if __name__ == '__main__':
    app.run(debug=True)