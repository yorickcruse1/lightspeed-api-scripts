import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

BASE_URL="https://api.lsk.lightspeed.app"
BUSINESS_LOCATION_ID=1231959829250050
# Define your date range here using ISO 8601 format
START = "2026-01-12T00:00:00Z"
END = "2026-02-04T00:00:00Z"

def get_all_shifts(location_id, start_time=None, end_time=None):
    if not API_TOKEN or not BASE_URL:
        print("Error: API_TOKEN or BASE_URL not found in .env file.")
        return None

    endpoint = f"{BASE_URL}/staff/v1/businessLocations/{location_id}/shift"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    all_shifts = []
    current_page = 1
    total_pages = 1

    print(f"--- Starting Retrieval for Location {location_id} ---")
    if start_time: print(f"Filtering after: {start_time}")
    if end_time: print(f"Filtering before: {end_time}")

    while current_page <= total_pages:
        # We add the new filters to the params dictionary
        params = {
            "page": current_page,
            "size": 100,
            "sort": "date,asc",
            "startTime": start_time,
            "endTime": end_time 
        }

        try:
            response = requests.get(endpoint, headers=headers, params=params)
            print(f"Requesting: {response.url}")
            response.raise_for_status()
            
            data = response.json()
            data_wrapper = data.get("data", {})
            batch = data_wrapper.get("shifts", [])
            
            all_shifts.extend(batch)

            pagination_info = data.get("page", {})
            total_pages = pagination_info.get("totalPages", 1)
            
            print(f"Page {current_page}/{total_pages}: Found {len(batch)} shifts.")
            current_page += 1

        except requests.exceptions.RequestException as e:
            print(f"API Request failed on page {current_page}: {e}")
            break

    return all_shifts

# --- Execution ---
if __name__ == "__main__":

    shifts = get_all_shifts(BUSINESS_LOCATION_ID, start_time=START, end_time=END)

    if shifts:
        file_path = Path.home() / "Desktop" / "get_shifts.json"
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(shifts, file, indent=4)
        
        print(f"\n✅ SUCCESS: {len(shifts)} filtered shifts saved to your Desktop!")
    else:
        print("\n❌ No data found for this date range.")