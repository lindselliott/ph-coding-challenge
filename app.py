from flask import Flask, request
import pydicom
import matplotlib.pyplot as plt
import matplotlib
import os
matplotlib.use('Agg')

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

EXPORT_FOLDER = './export'
app.config['EXPORT_FOLDER'] = EXPORT_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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


# Endpoint to upload DCM file - puts in /upload folder
@app.route('/upload', methods=['POST'])
def upload_file():
    # If file isnt in body - throw error
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    # If file is empty, throw error
    if file.filename == '':
        return 'No selected file', 400
    
    # Only accept (.dcm) files 
    if file: # and file.filename.endswith('.dcm'):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return f'File {filename} uploaded successfully', 200
    
    # Throw general error if any other issues
    return "Error uploading file", 400


# Get tag from file
@app.route('/tag',  methods=['GET'])
def get_tag():
    # Path to DICOM file
    file_name = request.args.get('file_name')  # Assuming file_id or filename is passed
    path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    
    if not os.path.exists(path):
        return 'File not found', 404

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

    except Exception as e:
        return f"Error reading DICOM file: {e}", 400
   
    # This doesnt have name in it so wondering if that is needed
    return value.to_json()


# Get get image from file and save as png
@app.route('/image',  methods=['GET'])
def get_png():
    # Path to DICOM file
    file_name = request.args.get('file_name')  # Assuming file_id or filename is passed
    path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    
    if not os.path.exists(path):
        return 'File not found', 404

    # Read DICOM dataset
    dicom_data = pydicom.dcmread(path)

    try:
        # render image
        dicom_data = dicom_data.pixel_array  

        # Save the image to a file
        plt.imshow(dicom_data, cmap='gray')
        plt.title("DICOM Image")
        plt.axis('off')

        # Create the folder if it doesn't exist
        os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)
        path = os.path.join(app.config['EXPORT_FOLDER'], file_name)

        plt.savefig(f"{path}.png", bbox_inches='tight')
        plt.close()  # Close the plot to free memory

    except Exception as e:
        return f"Error converting DICOM file to png: {e}", 400
    
    return f'File {file_name} saved as png to export folder', 200


# root
@app.route('/')
def home():
    return "Root"


if __name__ == '__main__':
    app.run(debug=True)