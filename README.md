
# CIS 6930, Spring 2024 Assignment 2 - Augmenting Data

## Author
Name: Priyanshu Mathur


## Introduction
This Python script performs data augmentation on police incident records extracted from PDF files. It enriches the dataset with additional information like day of the week, time of day, weather conditions, etc. The augmented data can be used for deeper analysis and preparation for further processing in a data pipeline.
## Running Instructions
To execute the data augmentation script (`assignment2.py`), follow the steps below.

1. **Setup Environment:**  
   Ensure Python 11 or newer is installed along with `pipenv` for handling virtual environments and dependencies.
   ```bash
   pip install pipenv
   ```

2. **Install Dependencies:**  
   Navigate to the project directory and install dependencies using:
   ```bash
   pipenv install
   ```

3. **Activate Virtual Environment:**  
   Activate the virtual environment with:
   ```bash
   pipenv shell
   ```
   Alternatively, use `pipenv run` before commands to run them directly within the virtual environment.

4. **Execute the Script:**  
   Use the following command to run `assignment2.py`:
   ```bash
   pipenv run python assignment2.py --urls files.csv
   ```
   Replace `<Path to CSV file with URLs>` with the actual file path. This CSV file should contain URLs to the PDFs of incident reports.

## Dependencies

- `argparse`: For parsing command-line arguments.
- `csv`: For reading CSV files.
- `src`: Custom module for utility functions.
- `requests`: For downloading files from URLs.
- `pypdf`: For reading PDF files.
- `os`: For interacting with the operating system.
- `random`: For generating random values.
- `base64`: For decoding the API key.
- `collections.Counter`: For counting occurrences of elements in a list.
- `geopy.geocoders.Photon`: For geocoding locations.
- `math`: For mathematical operations.
- `datetime.datetime`, `datetime.timedelta`: For working with dates and times.

## Functionality

The script provides the following functionalities for data augmentation:

- **PDF Download (`pdf_download(url)`)**: Downloads a PDF file from a given URL and saves it locally.
- **Data Extraction (`data_extract(pdf_path)`)**: Extracts incident records from a PDF file and cleans the data.
- **Location Ranking (`rank_locations(incidents)`)**: Ranks incident locations based on their frequency.
- **Day of Week and Time of Day Extraction (`get_day_of_week(date_time_str)`, `get_time_of_day(date_time_str)`)**: Extracts the day of the week and time of day from a date/time string.
- **Weather Checking (`check_weather(api_key, date_time_str)`)**: Checks the weather conditions for a given date/time using the OpenWeatherMap API.
- **Location Geocoding (`get_lat_lon_from_location(location_name)`)**: Geocodes a location name to latitude and longitude coordinates.
- **Bearing Calculation and Side of Town Determination (`calculate_bearing(...)`, `determine_side_of_town(bearing)`)**: Calculates the bearing and determines the side of town for an incident location.
- **Incident Nature Ranking (`calculate_incident_ranks(incidents)`)**: Assigns ranks to incident natures based on their frequency.
- **EMS Status Checking (`check_emsstat(incident, incidents, current_index)`)**: Checks if an incident involves an EMS status.
- **Data Augmentation (`augment_data(incidents, location_ranks, incident_ranks, api_key)`)**: Augments incident records with additional information.

Additionally, the script includes utility functions for parsing CSV files to extract URLs of incident PDFs and for printing augmented data to stdout.

Run:
**(`python script.py --urls files.csv`)**


## Test Descriptions

### test_time.py

- `test_get_day_of_week`: Tests the `get_day_of_week` function, which returns the numeric representation of the day of the week (1-7, where 1 is Sunday).
- `test_get_time_of_day`: Tests the `get_time_of_day` function, which returns the hour of the day (0-24) the incident was reported.

### test_geo.py

- `test_get_lat_lon_from_location`: Tests the `get_lat_lon_from_location` function, which returns the latitude and longitude coordinates of a given location.
- `test_calculate_bearing`: Tests the `calculate_bearing` function, which calculates the bearing (compass direction) between two sets of coordinates.
- `test_determine_side_of_town`: Tests the `determine_side_of_town` function, which determines the side of town (N, NE, E, SE, S, SW, W, NW) based on a given bearing.

### test_nature.py

- `test_calculate_incident_ranks`: Tests the `calculate_incident_ranks` function, which calculates the rank of each incident's nature based on frequency.
- `test_check_emsstat`: Tests the `check_emsstat` function, which checks if EMS (Emergency Medical Services) was dispatched for the current incident ORI or the next one or two records for the same time and location contain "EMSSTAT".

## Usage

To run the tests, use a test runner such as pytest:

```bash
pytest test_time.py
pytest test_geo.py
pytest test_nature.py
```

These test functions are located in the `tests/` directory and can be executed to verify the correctness of the respective functionalities.

## Reliability 
- **Reliability:** The script has undergone thorough testing to ensure its reliability. However, due to the complexity of real-world data, there may be unforeseen issues that could arise. Users are encouraged to test the script with their data and provide feedback for continuous improvement.

## Assumptions

- **PDF Format:** The script assumes that the incident reports are in a standard PDF format and can be parsed using the `PyPDF2` library. Any deviations from this format may cause parsing errors.

- **Data Integrity:** It is assumed that the incident reports provided are accurate and reliable. Any inconsistencies or errors in the reports may lead to incorrect data augmentation.

- **API Limitations:** The script assumes that there are no limitations or restrictions on the usage of external APIs, such as the OpenWeatherMap API, for weather data retrieval. Users should be aware of any API rate limits or access restrictions that may apply.

- **Location Accuracy:** The accuracy of geocoding locations using the Geopy library depends on the quality and specificity of the location names provided in the incident reports. Ambiguous or incomplete location names may result in inaccurate geocoding.

- **Weather Data Availability:** The script assumes that historical weather data is available for the specified locations and timestamps. Any gaps or inconsistencies in the weather data may affect the accuracy of the augmented data.

- **Incident Report Consistency:** It is assumed that incident reports follow a consistent format across different sources. Any variations or inconsistencies in the format may require adjustments to the parsing logic.

- **Data Privacy:** The script assumes that incident reports do not contain sensitive or personally identifiable information. Users should ensure compliance with data privacy regulations when using the script with real-world data.


## Resources
- A collection of Model Cards and Data Sheets: [[Link to resource](https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports)]
- Historical Weather API: [[Link to OpenWeatherMap API documentation](https://openweathermap.org/api)]
