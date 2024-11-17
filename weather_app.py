# DSC 510
# Week 12
# 12.1 Assignment Programming
# Author: Andrew Goodman
# Due Date: 11/16/2024

# Change Control Log
# Change #1
# Change(s) Made: Base File and Functions Created
# Author: Andrew Goodman
# Date of Change: 11/10/2024

# Change Control Log
# Change #2
# Change(s) Made: Updated names to match those in API documentation
# Author: Andrew Goodman
# Date of Change: 11/11/2024

# Change Control Log
# Change #3
# Change(s) Made: Fixed pretty print to give clearer printout
# Author: Andrew Goodman
# Date of Change: 11/13/2024

import requests

# Constants for API key, Geocoding API, and Weather Data API
API_KEY = 'API-KEY-GOES-HERE'
GEOCODING_URL = 'https://api.openweathermap.org/geo/1.0/direct'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_user_choice():
    """Displays the main menu and gets user's choice for lookup method."""
    # Prompt for user to select how they would like to look up weather
    print("\nWeather Forecast Application")
    print("----------------------------")
    print("1. Lookup by City and State")
    print("2. Lookup by US Zip Code")
    print("3. Exit")
    while True:
        choice = input("Please enter your choice (1-3): ").strip()
        if choice in ("1", "2", "3"):
            # Returns choice for main function to continue
            return choice
        else:
            print("Invalid input. Please enter a valid choice of 1, 2, or 3.")

def get_temperature_type():
    """Prompts the user to select temperature type."""
    # Prompt for user to select which temperature type they want
    print("\nSelect temperature type")
    print("1. Celsius")
    print("2. Fahrenheit")
    print("3. Kelvin")
    while True:
        # Based on prompt, returns what kind of temperature type they would like weather to be in
        temperature_type = input("Please enter temperature type (1-3): ").strip()
        if temperature_type == "1":
            # 'metric' corresponds to Celsius
            return 'metric'
        elif temperature_type == "2":
            # 'imperial' corresponds to Fahrenheit
            return 'imperial'
        elif temperature_type == "3":
            # 'standard' corresponds to Kelvin
            return 'standard'
        else:
            print("Invalid input. Please enter 1 for Celsius, 2 for Fahrenheit, or 3 for Kelvin.")

def get_location_by_city():
    """Prompts the user to enter city and state for weather lookup."""
    # List of valid US state codes
    valid_states = {
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    }
    while True:
        # User enters city and state code
        city = input("Please enter city: ").strip()
        state = input("Please enter state code (e.g., FL for Florida): ").strip().upper()
        # Checks state code is empty or invalid, informs user and starts process over
        if state not in valid_states:
            print("Invalid State Input. Please enter a valid state.")
            continue
        # If validations pass, return the location
        return {'city': city, 'state': state}

def get_location_by_zip():
    """Prompts the user to enter zip code for weather lookup."""
    zip_code = input("Please enter zip code: ").strip()
    if not zip_code.isdigit():
        # If zipcode is not only digits, prompts user to reenter code
        print("Invalid input. Please enter a valid numeric zip code.")
        return get_location_by_zip()
    return zip_code

def fetch_geocoding_data(location):
    """Fetches geographical coordinates based on city and state."""
    # Prepare query parameters to specify its United States
    params = {
        'q': f"{location['city']},{location['state']},US",
        'limit': 1,
        'appid': API_KEY
    }
    try:
        # Make a GET request with a timeout of 10 seconds
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            # If no data is returned, inform user
            raise ValueError("No location found with the provided city and state.")
        # Sets latitude and longitude from data
        latitude = data[0]['lat']
        longitude = data[0]['lon']
        # Returns the coordinates as a tuple
        return latitude, longitude
    # Error exceptions with error codes presented
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error during geocoding: {http_err}")
    except requests.exceptions.Timeout:
        raise Exception("Request timed out during geocoding.")
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"An error occurred during geocoding: {req_err}")
    except ValueError as val_err:
        raise Exception(val_err)

def fetch_weather_data_lat_lon(lat, lon, units):
    """Fetches weather data based on latitude and longitude."""
    # Prepare query parameters to for Weather API
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': units
    }
    try:
        # Get requests for Weather API
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    # Handles error exceptions with error codes presented
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error during weather data retrieval: {http_err}")
    except requests.exceptions.Timeout:
        raise Exception("Request timed out during weather data retrieval.")
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"An error occurred during weather data retrieval: {req_err}")

def fetch_weather_data_zip(zip_code, units):
    """Fetches weather data based on zip code."""
    # Prepare query parameters for country code 'US' to specify United States
    params = {
        'zip': f"{zip_code}, US",
        'appid': API_KEY,
        'units': units
    }
    try:
        # Get requests for Weather API
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    # Handles error exceptions with error codes presented
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error during weather data retrieval: {http_err}")
    except requests.exceptions.Timeout:
        raise Exception("Request timed out during weather data retrieval.")
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"An error occurred during weather data retrieval: {req_err}")

def pretty_print(weather_data, units):
    """Displays weather information in a readable format."""
    try:
        # Extract relevant weather information from API response
        location = f"{weather_data['name']}, {weather_data['sys']['country']}"
        current_temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        temp_min = weather_data['main']['temp_min']
        temp_max = weather_data['main']['temp_max']
        pressure = weather_data['main']['pressure']
        humidity = weather_data['main']['humidity']
        weather_description = weather_data['weather'][0]['description'].title()
        # Determine the temperature type symbol
        if units == 'metric':
            # Celsius
            temp_unit = '°C'
        elif units == 'imperial':
            # Fahrenheit
            temp_unit = '°F'
        else:
            # Kelvin
            temp_unit = 'K'
        # Display formatted weather information
        print("\nCurrent Weather Information")
        print("---------------------------")
        print(f"Location: {location}")
        print(f"Temperature: {current_temp}{temp_unit}")
        print(f"Feels Like: {feels_like}{temp_unit}")
        print(f"Low Temperature: {temp_min}{temp_unit}")
        print(f"High Temperature: {temp_max}{temp_unit}")
        print(f"Pressure: {pressure} hPa")
        print(f"Humidity: {humidity}%")
        print(f"Weather Description: {weather_description}")
    except KeyError as e:
        # Handle missing information from data fields based on API response
        print(f"Error parsing weather data: Missing key {e}")

def main():
    """Main program function for weather application."""
    # Initial greeting message
    print("Welcome to the US Weather Forecast Application")
    while True:
        # Captures the user's choice
        choice = get_user_choice()
        # Based on selection, displays a goodbye message
        if choice == "3":
            print("Thank you for using the US Weather Forecast Application.")
            break
        # Based on selection, asks to look up via zip code or city and state
        elif choice == "1":
            location = get_location_by_city()
            location_type = 'city'
        elif choice == "2":
            location = get_location_by_zip()
            location_type = 'zip'
        # Prompt to get the temperature type
        units = get_temperature_type()
        try:
            if location_type == 'city':
                # If lookup type is city, fetch geographical coordinates
                latitude, longitude = fetch_geocoding_data(location)
                # uses coordinates to gather weather data
                weather_data = fetch_weather_data_lat_lon(latitude, longitude, units)
            elif location_type == 'zip':
                # Checks to see lookup type is zip, fetch weather data directly
                weather_data = fetch_weather_data_zip(location, units)
            # Displays the weather data information in a readable format
            pretty_print(weather_data, units)
        except Exception as e:
            # Handles any exception errors and presents them
            print(f"Error: {e}")
        while True:
            # Prompt to allow user to perform more lookups
            repeat = input("\nWould you like to perform another lookup? (y/n): ").strip().lower()
            if repeat == "y":
                # If user continues, it breaks out of inner loop to restart main loop
                break
            elif repeat == "n":
                # If user exits, displays a message and terminate program
                print("Thank you for using the US Weather Forecast Application.")
                return
            else:
                # If y or n is not inputted, inform user and prompt again
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    main()