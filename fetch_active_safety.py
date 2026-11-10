import requests

URL = "https://vpic.nhtsa.dot.gov/api/vehicles/GetVehicleVariableList?format=json"


def fetch_vehicle_variables():
    """Fetch the full list of vehicle variables from the NHTSA API."""
    print("Loading car part data...")
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(f"Error fetching data: {error}")
        return None
    try:
        data = response.json()
    except ValueError:
        print("Error: the server did not return valid JSON.")
        return None
    return data.get("Results", [])

def filter_active_safety(variables):
    """Keep only items whose GroupName is exactly 'Active Safety System'."""
    return [item for item in variables if item.get("GroupName") == "Active Safety System"]


def main():
    variables = fetch_vehicle_variables()
    if variables is None:
        return
    active_safety = filter_active_safety(variables)
    print(f"\nFound {len(active_safety)} Active Safety System items:\n")
    for item in active_safety:
        print(f"- {item.get('Name')} (ID {item.get('ID')})")


if __name__ == "__main__":
    main()
