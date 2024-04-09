Name: Priyanshu Mathur

# Assignment Description
This Assignment is that we need to perform data augmentation on the extracted records from the previous assignment. To perform augmentation we will need to keep fairness and bias issues in mind. The task is to form a comprehensive pipeline for downloading, processing, augmenting, and storing incident data from PDFs sourced from URLs.


# How to install
1. Clone the repository on your system:
    
$ git clone https://github.com/mathurpriyanshu/cis6930sp24-assignment2.git

    
2. Install prerequisites:
$ pipenv install


# How to run
Branch to be used: main 

Command to run: 

pipenv run python assignment2.py --urls <filename>

# Functions

1. **`pdf_download(url)`**: This function downloads a PDF from a specified URL using HTTP GET, setting a user-agent header to mimic a browser request. It saves the PDF locally and returns the path to the downloaded file.

2. **`data_extract(pdf_path)`**: Extracts text from a given PDF file path. It uses the `pypdf.PdfReader` to read PDF pages and extracts text assuming a layout mode. It processes and returns data based on the text extracted from all pages.

3. **`determine_day_of_week(date_str)`**: Converts a date string into a `datetime` object and returns the weekday as an integer, where Monday is 1 and Sunday is 7.

4. **`determine_time_of_day(date_str)`**: Parses a datetime string to find the hour of the day (0-23), representing the time of day.

5. **`determine_weather(latitude, longitude, time)`**: Fetches weather conditions using an API by providing geographic coordinates and a timestamp. Handles API responses and errors, returning weather conditions or an error message.

6. **`rank_locations(locations)`**: Ranks locations based on their frequency of occurrence using a `Counter` from the collections module, assigning a rank to each unique location.

7. **`determine_side_of_town(location)`**: Uses the `Nominatim` service to geocode a location name and determines if it is within a central area or outside, based on a set radius.

8. **`rank_incidents(natures)`**: Ranks incident natures by frequency using a `Counter`, similarly to location ranking.

9. **`augment_data(data)`**: Augments incident records with additional attributes such as day of the week, time of day, weather conditions, location and incident ranks, and whether the incident type matches 'EMSSTAT'.

10. **`db_population(augmented_data)`**: Populates a SQLite database with the augmented incident data, handling database connection, table creation, and data insertion.

11. **`main(url)`**: Orchestrates the download, extraction, augmentation, and database population processes for incident data from a given URL.

 
## Bugs

1. **Error Handling**: Functions like `pdf_download` and `data_extract` may not handle all potential errors, such as network issues or corrupt PDF files, which can cause the program to crash.
2. **Database Transactions**: The `db_population` function lacks proper transaction management. If an error occurs during the insertion of records, it might partially commit data, leading to inconsistent database states.
3. **Date Parsing**: The `determine_day_of_week` and `determine_time_of_day` functions assume the date format is always correct and does not handle parsing errors which could occur if the input format varies.
4. **Weather API Dependency**: The `determine_weather` function assumes that the API will always return a 200 status and the expected weather data format. If the API changes or the network is down, this could result in unhandled exceptions or incorrect data handling.
5. **Geocoding Limitations**: The `determine_side_of_town` function may fail if the Nominatim service cannot find the location or if the API rate limits are exceeded.

## Assumptions
1. **PDF Text Extraction**: It is assumed that the text extraction from PDFs will always be accurate and that the layout mode sufficiently captures the data needed without formatting issues.
2. **Data Structure Consistency**: The data extraction logic assumes a consistent format in the text data, which may not always be the case, leading to incorrect parsing and data extraction.
3. **Stable Internet Connection**: The code assumes that the internet connection is stable and that the external APIs (weather, geocoding) will always be reachable and responsive.
4. **API Key and Limits**: The script assumes that a valid API key is available for the weather data API and that the request does not exceed the API's usage limits.
5. **Database Schema**: Assumes that the SQLite database schema does not change and that the table creation script correctly reflects the data structure used in the code.

To mitigate these issues, the code should include comprehensive error handling and validation checks to ensure that it can gracefully handle unexpected situations and input variations.

# Test Function Description

1. **`test_pdf_download`** verifies that the PDF download function can retrieve a file from a specified URL and save it correctly.
2. **`test_data_extract`** ensures that text extraction from a PDF works as intended, returning a list of data extracted from the document.
3. **`test_determine_day_of_week`** and **`test_determine_time_of_day`** test the correct parsing and computation of the day of the week and the hour from a given date-time string.
4. **`test_determine_weather`** checks the function that fetches weather data for given coordinates and time, ensuring it handles API interactions correctly.
5. **`test_rank_locations`** tests whether the location ranking system accurately assigns ranks based on the frequency of location occurrences.
6. **`test_determine_side_of_town`** assesses the geolocation function's ability to categorize a location as being in the center or outside of a predefined area.


