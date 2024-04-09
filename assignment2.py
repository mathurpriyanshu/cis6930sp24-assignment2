import os
import re
import sqlite3
import argparse
import urllib.request
from datetime import datetime
from collections import Counter
from geopy.geocoders import Nominatim
import requests

# Function to download PDF from URL
def pdf_download(url):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
    local_file_path = strings.file_paths["local_file_path"]
    with open(local_file_path, "wb") as local_file:
        local_file.write(data)

    return local_file_path

# Function to extract data from PDF
def data_extract(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text(extraction_mode="layout")

    lines = text.splitlines()
    lines = lines[2:]
    lines = lines[:-1]

    data = []
    for l in lines:
        if(l != ""):
            date_pattern = r'\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}'

            matches = re.finditer(date_pattern, l)

            if matches:
                indices = [match.start() for match in matches]
                matched_lines = [l[i:j].strip() for i, j in zip([0] + indices, indices + [None])]

                matched_lines = list(filter(None, matched_lines))
                for ml in matched_lines:
                    split_line = re.split("   ", ml)
                    non_empty_list = [value for value in split_line if value is not None and value != ""]
                    fields_extraction(non_empty_list, data)

            else:
                matched_lines =  [l.strip()]
                split_line = re.split("   ", l)

                non_empty_list = [value for value in split_line if value is not None and value != ""]
                fields_extraction(non_empty_list, data)

    return data

# Function to determine the day of the week
def determine_day_of_week(date_str):
    date_obj = datetime.strptime(date_str, "%m/%d/%Y %H:%M")
    return date_obj.weekday() + 1  # Monday is 1, Sunday is 7

# Function to determine the time of day
def determine_time_of_day(date_str):
    date_obj = datetime.strptime(date_str, "%m/%d/%Y %H:%M")
    return date_obj.hour

# Function to determine weather 
def determine_weather(latitude, longitude, time):
    api_key = "YOUR_OPEN_METEO_API_KEY"
    url = f"https://api.open-meteo.com/weather?latitude={latitude}&longitude={longitude}&timestamp={time}&hourly=wmo"

    try:
        response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
        if response.status_code == 200:
            weather_data = response.json()
            wmo_code = weather_data['hourly']['wmo']
            return wmo_code
        else:
            print(f"Failed to fetch weather data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to determine location rank
def rank_locations(locations):
    location_counter = Counter(locations)
    ranked_locations = {location: rank + 1 for rank, (location, _) in enumerate(location_counter.most_common())}
    return [ranked_locations[location] for location in locations]

# Function to determine side of town
def determine_side_of_town(location):
    geolocator = Nominatim(user_agent="incident_analysis")
    location_obj = geolocator.geocode(location)
    if location_obj:
        town_center = (35.220833, -97.443611)
        distance = geodesic(town_center, (location_obj.latitude, location_obj.longitude)).miles
        if distance < 5:  # Assuming town radius of 5 miles
            return 'Center'
        else:
            return 'Outside'
    else:
        return 'Unknown'

# Function to determine incident rank
def rank_incidents(natures):
    incident_counter = Counter(natures)
    ranked_incidents = {incident: rank + 1 for rank, (incident, _) in enumerate(incident_counter.most_common())}
    return [ranked_incidents[incident] for incident in natures]

# Function to perform data augmentation
def augment_data(data):
    augmented_data = []
    for record in data:
        day_of_week = determine_day_of_week(record['Date/Time'])
        time_of_day = determine_time_of_day(record['Date/Time'])
        weather = determine_weather()
        location_rank = record['Location Rank']
        side_of_town = determine_side_of_town(record['Location'])
        incident_rank = record['Incident Rank']
        nature = record['Nature']
        emsstat = True if record['Incident ORI'] == 'EMSSTAT' else False

        augmented_record = {
            'Day of the Week': day_of_week,
            'Time of Day': time_of_day,
            'Weather': weather,
            'Location Rank': location_rank,
            'Side of Town': side_of_town,
            'Incident Rank': incident_rank,
            'Nature': nature,
            'EMSSTAT': emsstat
        }
        augmented_data.append(augmented_record)

    return augmented_data

# Function to populate database with augmented data
def db_population(augmented_data):
    conn = sqlite3.connect('incident_data.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS incidents
                 (Day_of_Week INTEGER, Time_of_Day INTEGER, Weather INTEGER,
                 Location_Rank INTEGER, Side_of_Town TEXT, Incident_Rank INTEGER,
                 Nature TEXT, EMSSTAT INTEGER)''')

    # Insert data into table
    for record in augmented_data:
        c.execute("INSERT INTO incidents VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (record['Day of the Week'], record['Time of Day'], record['Weather'],
                   record['Location Rank'], record['Side of Town'], record['Incident Rank'],
                   record['Nature'], record['EMSSTAT']))

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Main function
def main(url):
    pdf_path = pdf_download(url)
    data = data_extract(pdf_path)
    augmented_data = augment_data(data)
    db_population(augmented_data)
    os.remove(pdf_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process incidents from a given URL.')
    parser.add_argument('--urls', help='File containing list of incident URLs')
    args = parser.parse_args()

    if args.urls:
        with open(args.urls, 'r') as file:
            urls = file.readlines()
            for url in urls:
                main(url.strip())
    else:
        print("Please provide the path to the file containing URLs using --urls option.")
