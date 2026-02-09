# Lightspeed API Scripts

A Python script to retrieve shift data from the Lightspeed API and export it as JSON.

## Overview

`get_shifts.py` fetches all shifts for a specified business location within a given date range from the Lightspeed K-Series API. The retrieved data is automatically saved to your Desktop as `get_shifts.json`.

## Prerequisites

- Python 3.7 or higher
- A valid Lightspeed API token
- The following Python packages:
  - `requests`
  - `python-dotenv`

## Installation

1. Clone or download this repository
2. Install required dependencies:
```bash
pip install requests python-dotenv
```

## Configuration

### Environment Variables

Create a `.env` file in the project root directory with your API credentials:

```
API_TOKEN=your_api_token_here
```

### Script Settings

Edit the following variables in `get_shifts.py` to customize your query:

- `BUSINESS_LOCATION_ID`: The Lightspeed business location ID (currently set to `1231959829250050`)
- `START`: Start date/time in ISO 8601 format (e.g., `"2026-01-12T00:00:00Z"`)
- `END`: End date/time in ISO 8601 format (e.g., `"2026-02-04T00:00:00Z"`)

## Usage

Run the script:

```bash
python get_shifts.py
```

The script will:
1. Authenticate with the Lightspeed API using your token
2. Retrieve all shifts for the specified location and date range
3. Display pagination progress in the console
4. Save the results to `~/Desktop/get_shifts.json`

### Example Output

```
--- Starting Retrieval for Location 1231959829250050 ---
Filtering after: 2026-01-12T00:00:00Z
Filtering before: 2026-02-04T00:00:00Z
Page 1/5: Found 100 shifts.
Page 2/5: Found 100 shifts.
...
✅ SUCCESS: 250 filtered shifts saved to your Desktop!
```

## Output

The script generates a JSON file containing an array of shift objects with the following structure:

```json
[
  {
    "id": "shift_id",
    "date": "2026-01-12",
    "startTime": "09:00:00",
    "endTime": "17:00:00",
    ...
  }
]
```

## Error Handling

The script includes error handling for:
- Missing API token or base URL
- API request failures
- Network issues

If an error occurs, check that:
1. Your `.env` file exists and contains a valid `API_TOKEN`
2. You have internet connectivity
3. Your API token is still valid
4. The `BUSINESS_LOCATION_ID` is correct

## Pagination

The script automatically handles pagination, retrieving up to 100 shifts per page and continuing until all available data is fetched.

## License

[Add your license here]
