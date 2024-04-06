
Name: Priyanshu Mathur

# Assignment Description
This Assignment is that we need to perform data augmentation on the extracted records from the previous assignment. To perform augmentation we will need to keep fairness and bias issues in mind.


# How to install
1. Clone the repository on your system:
    
$ git clone https://github.com/mathurpriyanshu/cis6930sp24-assignment2.git

    

2. Install prerequisites:
$ pipenv install pandas geopy


# How to run
Branch to be used: main 

Command to run: 

pipenv run python assignment2.py --urls <filename>

# Functions


1. `main(urls_file)`: This function serves as the entry point of the script. It takes a file containing a list of incident URLs as input. It extracts data from each PDF file corresponding to the URLs, performs data augmentation on the extracted data, and prints the augmented data in a tab-separated format. It integrates the functionalities of other functions to achieve this.

2. `pdf_download(url)`: This function downloads a PDF file from a given URL. It uses `urllib.request.urlopen()` to fetch the PDF content and saves it locally. It returns the local file path where the PDF is saved.

3. `data_extract(pdf_path)`: This function extracts data from a given PDF file. It uses `PyPDF2` to read the PDF content and extract text from each page. Then, it processes the text to extract incident-related information such as date/time, incident number, location, nature, etc. It returns a list of dictionaries, where each dictionary represents an incident record.

4. `determine_side_of_town(location)`: This function determines the side of town based on the location coordinates. It uses `geopy` to obtain the coordinates of the town center and compares them with the coordinates of the incident location to determine the side (N, S, E, W, NW, NE, SW, SE).

5. `rank_locations(locations)`: This function ranks the locations based on their frequency in the dataset. It uses `Counter` from the `collections` module to count the occurrences of each location and assigns a rank accordingly.

6. `augment_data(data)`: This function performs data augmentation on the extracted incident data. It takes the extracted data as input and augments it according to the specifications provided in the assignment. For demonstration purposes, it currently returns dummy augmented data.

These functions collectively handle the extraction, processing, augmentation, and printing of incident data from PDF files based on the provided URLs.






# Bugs

1. Error Handling: The code lacks robust error handling mechanisms. If there are issues with downloading PDFs, extracting data, or performing data augmentation, the script may fail without providing clear error messages.
2. PDF Parsing Issues: The code relies on PyPDF2 for PDF parsing, which may not handle all PDF formats perfectly. There could be cases where the extraction of text from PDFs may fail or produce incorrect results.
3. URL File Handling: The code assumes that the URLs file provided via the `--urls` option is properly formatted and contains valid URLs. If the file format is incorrect or URLs are malformed, it may cause unexpected behavior.
4. PDF File Deletion: The code deletes PDF files immediately after extracting data. If the subsequent data augmentation process fails, there's no way to re-extract data from the PDFs without downloading them again.


# Assumptions
1. Data Structure: The data extraction assumes a specific structure/format of incident data within the PDF files. If the structure/format varies across different PDFs, the extraction process may fail or produce inaccurate results.
2. Side of Town Determination: The function `determine_side_of_town()` assumes a simplistic approach to determine the side of town based on coordinates. It considers only cardinal directions (N, S, E, W) and divides the town into quadrants. This may not accurately represent the actual side of town in more complex geographic layouts.
3. Data Augmentation Logic: The `augment_data()` function currently returns dummy augmented data for demonstration purposes. The actual data augmentation logic based on the provided specifications is missing. Implementing the correct logic based on the specifications is crucial for generating meaningful augmented data.
4. Geolocation Accuracy: The code assumes that geolocation services (e.g., Nominatim) provide accurate results for determining the town center's coordinates. In practice, the accuracy of geolocation services may vary, leading to inaccuracies in determining the side of town.

# Test Function Description


1. **test_pdf_download**: This test function would verify that PDF files can be downloaded from provided URLs successfully. It would simulate different scenarios such as valid URLs, invalid URLs, network errors, and ensure that appropriate error handling is in place.

2. **test_data_extraction**: This function would test the data extraction process from PDF files. It would use sample PDF files with known content and verify that the extraction function correctly parses and extracts incident data. Test cases would cover various scenarios such as single-page PDFs, multi-page PDFs, different text layouts, and edge cases.

3. **test_side_of_town_determination**: This test function would validate the accuracy of the `determine_side_of_town()` function. It would provide known coordinates representing different sides of town and verify that the function correctly assigns the corresponding side (N, S, E, W, NW, NE, SW, SE).

4. **test_rank_locations**: This function would test the accuracy of the `rank_locations()` function. It would provide a sample list of locations with known frequencies and verify that the function ranks them correctly based on frequency. Test cases would include locations with different frequencies and ties.

5. **test_augment_data**: This test function would validate the data augmentation process. It would compare the augmented data generated by the `augment_data()` function against expected results based on known input data and specifications. Test cases would cover different combinations of incident data and expected augmented attributes.

6. **test_integration**: This function would perform end-to-end testing of the entire workflow, from downloading PDFs to printing augmented data. It would use sample input URLs, mock PDF files, and expected augmented data to validate the entire process. This test would ensure that all components work together correctly.
