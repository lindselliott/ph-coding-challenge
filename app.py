from flask import Flask, request
import pydicom
import matplotlib.pyplot as plt

app = Flask(__name__)

# Recursive function to find the tag
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

def convert_to_png(dicom_data):
    if 'PixelData' in dicom_data:
        print("Pixel data found.")
    else:
        print("Pixel data not found in this DICOM file.")

    # new_image = dicom_data.pixel_array.astype(float)
    # print(new_image)

    # plt.imshow(dicom_data.pixel_array, cmap=plt.cm.gray)
    # plt.show()


@app.route('/')
def home():
    # Path to DICOM file
    path = "test_files/XRAY/DICOMDIR"

    # Get the DICOM tag requested in the query parameter 'tag'
    tag = request.args.get('tag')

    # Read DICOM dataset
    dicom_data = pydicom.dcmread(path)

    try:
        # Convert the tag into an integer (DICOM tags are integers)
        tag_int = int(tag, 16)
        value = find_tag(tag_int, dicom_data, indent="")
        # print(value)   

        if value == -1:
            return f"Tag not found in DICOM file: {tag}", 201
        
        # commenting this out as I was not able to test a DICOM with PixelData
        # convert_to_png(dicom_data)

    except Exception as e:
        return f"Error reading DICOM file: {e}", 400
   
    # This doesnt have name in it so wondering if that is needed
    return value.to_json()


if __name__ == '__main__':
    app.run(debug=True)