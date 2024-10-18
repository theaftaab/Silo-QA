# Checking Json response for QA test pass/fail

from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
import os
import re

# Path to the QA folder on the desktop
base_folder_path = os.path.expanduser("~/Desktop/QA1")

# Initialize global counters for passed and failed QA
total_passed = 0
total_failed = 0


# Function to classify image types based on file names
def classify_image(img):
    if re.search(r'[sS]', img):
        return 'side'
    elif re.search(r'[rR]', img):
        return 'rear'
    elif re.search(r'[fF]', img):
        return 'front'
    return None


# Function to process each folder dynamically
def process_folder(folder_path):
    global total_passed, total_failed  # Declare the global c
    image_paths = {}

    # Loop through the files in the folder
    for img_file in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_file)
        if os.path.isfile(img_path) and img_file.lower().endswith(('.jpeg', '.jpg', '.png')):
            img_type = classify_image(img_file)
            if img_type and img_type not in image_paths:  # Only take the first occurrence of each type
                image_paths[img_type] = img_path
                if len(image_paths) == 3:  # Stop after finding 3 images
                    break

    # If we don't have all 3 images, we can't proceed
    if len(image_paths) < 3:
        print(f"Not enough images in folder: {folder_path}")
        return

    # Prepare files for MultipartEncoder
    fields = {f'{img}-img': (os.path.basename(path), open(path, 'rb'), 'image/jpeg') for img, path in
              image_paths.items()}
    fields['language'] = "en"

    # Using MultipartEncoder
    m = MultipartEncoder(fields=fields)

    # Headers
    headers = {
        'Content-Type': m.content_type,
        'Accept': 'application/json'
    }

    # API endpoint
    api_url = "https://dev-scanner.silofortune.com/api/v2/cattle-scanner"

    # Make API call (POST request)
    response = requests.post(api_url, data=m, headers=headers)

    # Print status code and full response for debugging
    print(f"Status Code: {response.status_code}")
    print("Response Text:", response.text)

    try:
        # Check if the response status is 200 (QA passed) or not
        if response.status_code == 200:
            total_passed += 1  # Increment the global passed counter
            print("QA Passed")
        elif response.status_code == 400:
            print("QA Failed")
            total_failed += 1  # Increment the global passed counter
        else:
            print("Internal server error")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close all opened files
        for file_tuple in fields.values():
            if isinstance(file_tuple, tuple):
                file_tuple[1].close()  # Close the file object


# Loop through all folders dynamically
for folder_name in os.listdir(base_folder_path):
    folder_path = os.path.join(base_folder_path, folder_name)

    if os.path.isdir(folder_path):  # Process only folders
        print(f"Processing folder: {folder_name}")
        process_folder(folder_path)

# After all folders are processed, print the total passed and failed
print(f"\nTotal number of QA Passed: {total_passed}")
print(f"Total number of QA Failed: {total_failed}")