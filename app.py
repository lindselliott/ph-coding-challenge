from flask import Flask, request
import pydicom
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

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

# Function to take in a DCM and generate a png and save that
def convert_to_png(image_data):
    image_data = image_data.pixel_array  

    # Save the image to a file
    plt.imshow(image_data, cmap='gray')
    plt.title("DICOM Image")
    plt.axis('off')
    plt.savefig("output_image.png", bbox_inches='tight')
    plt.close()  # Close the plot to free memory


@app.route('/')
def home():
    # Path to DICOM file
    path = "test_files/XRAY/DICOMDIR"
    image = "test_files/IM000001"

    # Get the DICOM tag requested in the query parameter 'tag'
    tag = request.args.get('tag')

    # Read DICOM dataset
    dicom_data = pydicom.dcmread(path)
    image_data = pydicom.dcmread(image)

    try:
        # Convert the tag into an integer (DICOM tags are integers)
        tag_int = int(tag, 16)
        value = find_tag(tag_int, dicom_data, indent="")
        # print(value)   

        if value == -1:
            return f"Tag not found in DICOM file: {tag}", 201
        
        # Call function to save as a png
        convert_to_png(image_data)

    except Exception as e:
        return f"Error reading DICOM file: {e}", 400
   
    # This doesnt have name in it so wondering if that is needed
    return value.to_json()


if __name__ == '__main__':
    app.run(debug=True)