import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# 1. Load variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_TOKEN = os.getenv("API_TOKEN") 
BUSINESS_LOCATION_ID = os.getenv("BUSINESS_LOCATION_ID")

def get_all_shifts(location_id):
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

    while current_page <= total_pages:
        params = {
            "page": current_page,
            "size": 50,
            "sort": "date,asc"
        }

        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Navigate the nested structure: data -> shifts
            data_wrapper = data.get("data", {})
            batch = data_wrapper.get("shifts", [])
            
            all_shifts.extend(batch)

            # Update pagination logic from the root 'page' object
            pagination_info = data.get("page", {})
            total_pages = pagination_info.get("totalPages", 1)
            
            print(f"Page {current_page}/{total_pages}: Found {len(batch)} shifts.")
            current_page += 1

        except requests.exceptions.RequestException as e:
            print(f"API Request failed on page {current_page}: {e}")
            break

    return all_shifts

# --- Execution & Saving ---
if __name__ == "__main__":
    shifts = get_all_shifts(BUSINESS_LOCATION_ID)

    if shifts:
        file_path = Path.home() / "Desktop" / "shifts_output.json"

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(shifts, file, indent=4)
        
        print(f"\n✅ SUCCESS: {len(shifts)} total shifts saved to your Desktop!")
    else:
        print("\n❌ No data found to save.")