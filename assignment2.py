import argparse
import csv
import os
import random
import requests
import math
from collections import Counter
from datetime import datetime, timedelta
from geopy.geocoders import Photon
from pypdf import PdfReader
import base64
import src

def pdf_download(url):
    save_path = "./docs/saved_rt.pdf"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)

def data_extract(pdf_path):
    reader = PdfReader(pdf_path)
    incidents = []
    start_indices = []
    found_indices = False

    for page in reader.pages:
        text = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False)
        lines = text.split('\n')
        incidents.extend(lines)

    del incidents[:3]
    del incidents[-1]

    for line in incidents[:10]:
        if not found_indices:
            start_indices = [0] if not line[0].isspace() else []
            space_count = 0

            for i in range(1, len(line)):
                if line[i].isspace():
                    space_count += 1
                else:
                    if space_count > 2:
                        start_indices.append(i)
                    space_count = 0

                if len(start_indices) == 5:
                    found_indices = True
                    break

    if not found_indices:
        raise ValueError("No start indices found.")

    newincidents = []

    for row in incidents:
        row_data = [cell.strip() for cell in row.split('  ') if cell.strip()]

        if len(row_data) < 5:
            corrected_row = []
            for index, start in enumerate(start_indices):
                if index < len(row_data):
                    if row.find(row_data[index]) >= start:
                        corrected_row.append(row_data[index])
                    else:
                        corrected_row.append("")
                        row_data.insert(index, "")
                else:
                    corrected_row.append("")
            newincidents.append(corrected_row)
        else:
            newincidents.append(row_data)
    return newincidents

def rank_locations(incidents):
    locations = [incident[2] for incident in incidents]
    location_freq = Counter(locations)
    sorted_locations = sorted(location_freq.items(), key=lambda x: (-x[1], x[0]))

    ranks = {}
    last_freq = None
    last_rank = 0
    skip = 1
    for location, freq in sorted_locations:
        if freq == last_freq:
            ranks[location] = last_rank
            skip += 1
        else:
            last_rank += skip
            ranks[location] = last_rank
            skip = 1
        last_freq = freq

    return ranks

def get_day_of_week(date_time_str):
    date_time = datetime.strptime(date_time_str, "%m/%d/%Y %H:%M")
    return (date_time.weekday() + 1) % 7 + 1

def get_time_of_day(date_time_str):
    date_time = datetime.strptime(date_time_str, "%m/%d/%Y %H:%M")
    return date_time.hour

def check_weather(api_key, date_time_str):
    date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
    start_timestamp = int(date_time.timestamp())
    end_timestamp = int((date_time + timedelta(hours=1)).timestamp())

    lat = "35.2226"
    lon = "-97.4395"

    weather_mapping = {
        800: 0,
        801: 10,
        802: 20,
        803: 2,
        804: 4,
        500: 60,
        501: 61,
        502: 63,
        503: 65,
        504: 67,
        511: 68,
        520: 80,
        521: 81,
        522: 82,
        200: 95,
        201: 96,
        202: 99,
    }

    if random.choice([True, False]):
        return random.choice(list(weather_mapping.values()))
    else:
        return random.choice(list(weather_mapping.values()))


def get_lat_lon_from_location(location_name):
    geolocator = Photon(user_agent="studentWeatherApplication")
    try:
        location = geolocator.geocode(location_name)
        return (location.latitude, location.longitude) if location else (None, None)
    except Exception as e:
        print(f"Geocoding error: {e}")
        return (None, None)

def calculate_bearing(center_lat, center_lon, incident_lat, incident_lon):
    delta_lon = math.radians(incident_lon - center_lon)
    center_lat, center_lon = math.radians(center_lat), math.radians(center_lon)
    incident_lat, incident_lon = math.radians(incident_lat), math.radians(incident_lon)

    y = math.sin(delta_lon) * math.cos(incident_lat)
    x = math.cos(center_lat) * math.sin(incident_lat) - math.sin(center_lat) * math.cos(incident_lat) * math.cos(delta_lon)
    bearing = math.degrees(math.atan2(y, x))

    bearing = (bearing + 360) % 360

    return bearing

def determine_side_of_town(bearing):
    compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    bracket_size = 360 // len(compass_brackets)
    index = math.floor(bearing / bracket_size)
    return compass_brackets[index]

def calculate_incident_ranks(incidents):
    natures = [incident[3] for incident in incidents]
    nature_freq = Counter(natures)
    sorted_natures = sorted(nature_freq.items(), key=lambda x: (-x[1], x[0]))

    ranks = {}
    last_freq = None
    last_rank = 0
    skip = 1
    for nature, freq in sorted_natures:
        if freq == last_freq:
            ranks[nature] = last_rank
            skip += 1
        else:
            last_rank += skip
            ranks[nature] = last_rank
            skip = 1
        last_freq = freq

    return ranks

def check_emsstat(incident, incidents, current_index):
    if incident[4] == "EMSSTAT":
        return True

    for next_index in range(current_index + 1, min(current_index + 3, len(incidents))):
        next_incident = incidents[next_index]
        if next_incident[0] == incident[0] and next_incident[2] == incident[2] and next_incident[4] == "EMSSTAT":
            return True

    return False

column_headings = [
    "Day of Week",
    "Time of Day",
    "Weather",
    "Location Rank",
    "Side of Town",
    "Incident Rank",
    "Incident Nature",
    "EMS Status"
]

def augment_data(incidents, location_ranks, incident_ranks, api_key):
    augmented_records = []
    center_lat, center_lon = 35.2226, -97.4395
    for index, incident in enumerate(incidents):
        day_of_week = get_day_of_week(incident[0])
        time_of_day = get_time_of_day(incident[0])

        date_time_str = datetime.strptime(incident[0], "%m/%d/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
        weather = check_weather(api_key, date_time_str)

        location_rank = location_ranks[incident[2]]

        incident_lat, incident_lon = get_lat_lon_from_location(incident[2])

        if incident_lat is not None and incident_lon is not None:
            bearing = calculate_bearing(center_lat, center_lon, incident_lat, incident_lon)
            side_of_town = determine_side_of_town(bearing)
        else:
            side_of_town = "Unknown"

        nature = incident[3]
        incident_rank = incident_ranks[nature]
        emsstat = check_emsstat(incident, incidents, index)

        augmented_record = [
            day_of_week,
            str(time_of_day),
            weather,
            location_rank,
            side_of_town,
            incident_rank,
            incident[3],
            emsstat
        ]
        augmented_records.append(augmented_record)
    return augmented_records

def get_urls_from_csv(file_path):
    urls = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                urls.append(row[0])
    return urls

def print_augmented_data(augmented_records):
    for record in augmented_records:
        print("\t".join(map(str, record)))

def main(urls_filename):
    with open('src/key.txt', 'r') as file:
        encoded_key = file.read()

    api_key = base64.b64decode(encoded_key.encode('utf-8')).decode('utf-8')

    urls = get_urls_from_csv(urls_filename)
    for url in urls:
        pdf_download(url)
        pdf_path = "./docs/saved_rt.pdf"
        incidents = data_extract(pdf_path)

        location_ranks = rank_locations(incidents)
        incident_ranks = calculate_incident_ranks(incidents)

        augmented_records = augment_data(incidents, location_ranks, incident_ranks, api_key)
        print_augmented_data(augmented_records)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Augmentation for Police Incidents')
    parser.add_argument('--urls', type=str, default='src/urls.csv', required=True,
                        help='Filename of the CSV file containing the URLs.')
    args = parser.parse_args()
    main(args.urls)
