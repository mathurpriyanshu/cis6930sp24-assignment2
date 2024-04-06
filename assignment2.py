import argparse
import pandas as pd
from geopy.geocoders import Nominatim
from collections import Counter

# Import functions from Assignment 0
from assignment0 import pdf_download, data_extract

# Function to determine the side of town
def determine_side_of_town(location):
    geolocator = Nominatim(user_agent="assignment2")
    town_center = geolocator.geocode("Norman, OK")
    if location.latitude > town_center.latitude:
        if location.longitude > town_center.longitude:
            return 'NE'
        else:
            return 'NW'
    else:
        if location.longitude > town_center.longitude:
            return 'SE'
        else:
            return 'SW'

# Function to rank locations based on frequency
def rank_locations(locations):
    location_counter = Counter(locations)
    ranked_locations = {location: rank + 1 for rank, (location, _) in enumerate(location_counter.most_common())}
    return [ranked_locations[location] for location in locations]

# Function to perform data augmentation
def augment_data(data):
    # Augmented data columns
    augmented_columns = ['Day of the Week', 'Time of Day', 'Weather', 'Location Rank',
                         'Side of Town', 'Incident Rank', 'Nature', 'EMSSTAT']

    # Dummy values for demonstration
    augmented_data = [
        [1, 12, 201, 1, 'N', 1, 'Theft', True],
        [2, 15, 203, 2, 'S', 2, 'Assault', False],
        [3, 10, 202, 3, 'E', 3, 'Vandalism', True]
    ]

    augmented_df = pd.DataFrame(augmented_data, columns=augmented_columns)
    return augmented_df

def main(urls_file):
    # Extract data from PDFs
    data = []
    with open(urls_file, 'r') as file:
        for line in file:
            url = line.strip()
            pdf_path = pdf_download(url)
            data += data_extract(pdf_path)
            os.remove(pdf_path)  # Remove downloaded PDF file

    # Perform data augmentation
    augmented_data = augment_data(data)

    # Print augmented data
    print(augmented_data.to_csv(index=False, sep='\t'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform data augmentation on extracted records.')
    parser.add_argument('--urls', type=str, help='File containing list of incident URLs')
    args = parser.parse_args()

    if args.urls:
        main(args.urls)
    else:
        print("Please provide the path to the file containing URLs using --urls option.")
