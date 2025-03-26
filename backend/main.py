import requests
import pandas as pd
from datetime import datetime
import json
import os

# GraphQL endpoint
SPACEX_API_URL = "https://spacex-api.fly.dev/graphql"

# Your GraphQL query
LAUNCHES_QUERY = """
query {
  launches(limit: 200) {
    mission_name
    launch_date_utc
    launch_success
    launch_year
    launch_site {
      site_id
      site_name_long
      site_name
    }
    details
    rocket {
      rocket_name
      rocket_type
    }
  }
  payloads {
    id
    nationality
    payload_mass_kg
    payload_type
    manufacturer
    payload_mass_lbs
    customers
    reused
  }
}
"""
current_dir = os.path.dirname(__file__)
folder_path = os.path.join(current_dir, 'data')
def fetch_spacex_data():
    """Fetch launch data from SpaceX GraphQL API"""
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        SPACEX_API_URL,
        headers=headers,
        json={'query': LAUNCHES_QUERY}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

def transform_launch_data(data):
   
    # Load the data 
    launches = pd.json_normalize(data['data']['launches'], sep='_')
    payloads = pd.json_normalize(data['data']['payloads'], sep='_')


    # Convert 'launch_date_utc' to datetime and remove timezone information
    launches['launch_date_utc'] = pd.to_datetime(launches['launch_date_utc']).dt.tz_localize(None)

    # Extract rocket details into separate columns
    launches["rocket_name"] = launches["rocket_rocket_name"]
    launches["rocket_type"] = launches["rocket_rocket_type"]
    launches.drop(columns=["rocket_rocket_name", "rocket_rocket_type"], inplace=True)

    launches["launch_site_name"] = launches["launch_site_site_name"]
    launches["launch_site_long"] = launches["launch_site_site_name_long"]
    launches.drop(columns=["launch_site_site_name", "launch_site_site_name_long"], inplace=True)

    payloads.drop(columns=["payload_mass_lbs"], inplace=True)  # Remove redundant columns
    payloads["reused"] = payloads["reused"].astype(int)
    payloads = payloads.explode("customers")  # Flatten customer lists


    # Merge launches with payloads based on mission name and id
    merged_data = pd.merge(launches, payloads, left_on='mission_name', right_on='id', how='left')

    file_path_merged = os.path.join(folder_path, 'merged_data.xlsx')
    merged_data.to_excel(file_path_merged, index=False)
    return pd.DataFrame(merged_data)

def clean_launch_data(merged_data):

    merged_data['launch_success'] = merged_data['launch_success'].astype(bool)
    # Fill missing 'launch_success' with False (if appropriate)
    merged_data['launch_success'] = merged_data['launch_success'].fillna(False)

    # Fill numeric columns (e.g., payload_mass_kg) with the column mean
    merged_data['payload_mass_kg'] = merged_data['payload_mass_kg'].fillna(merged_data['payload_mass_kg'].mean())



    # Drop duplicate rows
    merged_data  = merged_data.drop_duplicates()

    file_path_clean = os.path.join(folder_path, 'after_clean.xlsx')
    merged_data.to_excel(file_path_clean, index=False)

    return merged_data 

def calculate_metrics(df):

    # 1. Total Launches
    total_launches = len(df)

    # 2. Overall Success Rate
    success_rate = df['launch_success'].mean() * 100

    # 3. Success Rate by Nationality
    success_rate_by_nationality = df.groupby('nationality')['launch_success'].mean() * 100
    success_rate_by_nationality = success_rate_by_nationality.round(2).to_dict()

    # 4. Percentage of Reused Rockets
    total_reused = df['reused'].sum()
    percentage_reused = (total_reused / total_launches) * 100

    # 5. Average Payload Mass
    average_payload_mass_success = df[df['launch_success'] == True]['payload_mass_kg'].mean()
    average_payload_mass_mass_failure = df[df['launch_success'] == False]['payload_mass_kg'].mean()

    # 6. Distribution of Payload Types
    payload_type_distribution = df['payload_type'].value_counts().to_dict()

    # 7. Launches by Rocket Type
    launches_by_rocket_type = df['rocket_type'].value_counts().to_dict()

    # 8. Launch Frequencies per Year
    launch_counts = df['launch_year'].value_counts().sort_index().to_dict()

    # Create the structured data
    launchData = {
        "totalLaunches": total_launches,
        "successRate": round(success_rate, 2),
        "successRateByNationality": success_rate_by_nationality,
        "reusedRocketsPercentage": round(percentage_reused, 2),
        "payloadTypeDistribution": payload_type_distribution,
        "launchesByRocketType": launches_by_rocket_type,
        "avgPayloadMass": {
            "successfulLaunches": round(average_payload_mass_success, 2),
            "failedLaunches": round(average_payload_mass_mass_failure, 2)
        },
        "launchFrequencyByYear": launch_counts
    }
    
    # Save the structured data to a JSON file

    file_path_json = os.path.join(folder_path, 'launch_data.json')

    try:
        # Ensure the 'data' folder exists, create it if not
        if not os.path.exists(file_path_json):
            os.makedirs(folder_path)
        
        # Write data to the JSON file
        with open(file_path_json, 'w') as json_file:
            json.dump(launchData, json_file, indent=2)
        
    except Exception as e:
        print(f"An error occurred: {e}")

    print("Metrics saved to launch_data.json")
    return 'metrics_df'



def run_initial_logic():
    try:
        # Step 1: Fetch data from SpaceX API
        raw_data = fetch_spacex_data()
        
        # Step 2: Transform the data
        df = transform_launch_data(raw_data)
        
        # Step 3: Cleaning the data
        cleaned_data = clean_launch_data(df)

        #Step 4: Creating metrix 
        calculate_metrics(cleaned_data)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    run_initial_logic()