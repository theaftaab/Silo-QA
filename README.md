**Automated Cattle Image QA Testing**
**Overview:**
This script automates the QA process for a cattle image classification API. It dynamically processes images from multiple folders, classifies them based on filenames, 
uploads them to the API, and evaluates the QA results based on the API response.

**Key Functionalities:**
1. **Folder & Image Processing:**
The script dynamically scans through a main folder containing subfolders of images.
Each image is classified as a 'side', 'rear', or 'front' image based on characters in the filename (S/s, R/r, F/f).

2.**API Request:**
The script waits for a response from the server and checks the status of each request, classifying the QA results as either "Passed" or "Failed."

3. **Logging & Summary:**
At the end of execution, it provides a summary of how many folders passed and how many failed based on the API response.

4. **Handling Response:**
If the status code is 200, the test is considered Passed.
If the status code is 400, the test is considered Failed.
Any other status code indicates a potential server error.

**Important Note:**
The dataset must be saved on the desktop inside a folder named QA1 (or a specified path in the script).
Numeric values are allowed in the image filenames alongside F, S, or R (e.g., 1234f.jpg or 123S.jpeg), but no other letters should be present after/before F, S, or R.
