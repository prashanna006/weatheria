from flet import *
import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

load_dotenv(override=True)
api_key = os.getenv('WEATHER_API_KEY')
response = requests.get(f"https://api.weather.com/v1/forecast?apiKey={api_key}&location=Miami")
print(response.json())  # Check if this works

def default_values(all_values):
    all_values[0].value = None
    all_values[1].value = "City_Name"
    all_values[2].value = f"--°F"
    all_values[3].value = f"--°F"
    all_values[4].value = f"--°F"
    all_values[5].value = "Weather Desc."
    all_values[6].value = f"Feels like --°F"
    all_values[7].value = "--:-- AM"
    all_values[8].value = "--:-- PM"
    
    # Update weather details
    all_values[9].value = f"-- km/hr"         # wind_text
    all_values[10].value = f"-- %"        # humidity_text
    all_values[11].value = f"-- hPa"      # pressure_text
    all_values[12].value = f"-- m"      # visibility_text
    all_values[13].value = f"-- m"         # sea_lvl_text
    all_values[14].value = f"-- m"      # ground_lvl_text

    # Update all Text fields in the UI
    for field in all_values[1:]:
        field.update()

def display_error(error, all_values):
    error_text = all_values[-1]
    error_text.value = error
    error_text.color = colors.RED_600
    error_text.update()
    default_values(all_values)

# Convert Unix timestamp to specified timezone with offset
def convert_to_timezone(timestamp, timezone_offset):
    # Convert to UTC datetime with timezone awareness, then apply the timezone offset
    utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time.strftime('%I:%M %p')

def display_weather(weather_values, all_values, timezone):
    # Unpack weather values
    city_name, current_temp, max_temp, min_temp, weather_desc, feels_like, sunrise, sunset, wind_value, humidity_value, pressure_value, visibility_value, sea_lvl_value, ground_lvl_value = weather_values
    sunrise_time = convert_to_timezone(sunrise, timezone)
    sunset_time = convert_to_timezone(sunset, timezone)
    # Update each specific Text field
    all_values[1].value = city_name
    all_values[2].value = f"{round(int(current_temp))}°F"
    all_values[3].value = f"{round(int(max_temp))}°F"
    all_values[4].value = f"{round(int(min_temp))}°F"
    all_values[5].value = weather_desc
    all_values[6].value = f"Feels like {round(int(feels_like))}°F"
    all_values[7].value = sunrise_time
    all_values[8].value = sunset_time
    
    # Update weather details
    all_values[9].value = f"{wind_value} km/hr"         # wind_text
    all_values[10].value = f"{humidity_value} %"        # humidity_text
    all_values[11].value = f"{pressure_value} hPa"      # pressure_text
    all_values[12].value = f"{visibility_value} m"      # visibility_text
    all_values[13].value = f"{sea_lvl_value} m"         # sea_lvl_text
    all_values[14].value = f"{ground_lvl_value} m"      # ground_lvl_text

    # Update all Text fields in the UI
    for field in all_values[1:]:
        field.update()
    all_values[0].value = None
    all_values[0].update()
    all_values[-1].value = None
    all_values[-1].update()

        

def get_weather(all_values):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={all_values[0].value}&appid={api_key}&units=imperial"
        response = requests.get(url)
        response.raise_for_status()  # This line will raise an exception for HTTP errors
        data = response.json()
        
        if data["cod"] == 200:
            weather_values = [data["name"], data["main"]["temp"], data["main"]["temp_max"], data["main"]["temp_min"], data["weather"][0]["description"], data["main"]["feels_like"], data["sys"]["sunrise"], data["sys"]["sunset"], data["wind"]["speed"], data["main"]["humidity"], data["main"]["pressure"], data["visibility"], data["main"]["sea_level"], data["main"]["grnd_level"]]
            display_weather(weather_values, all_values, data["timezone"])

    except requests.exceptions.HTTPError as http_err:
        status_code = response.status_code
        match status_code:
            case 400:
                display_error("Bad Request: Please Check Your Input", all_values)
            case 401:
                display_error("Unauthorized: Invalid API Key", all_values)
            case 403:
                display_error("Forbidden: Access Denied", all_values)
            case 404:
                display_error("Not Found: City Not Found", all_values)
            case 500:
                display_error("Internal Server Error: Please Try Again Later", all_values)
            case 502:
                display_error("Bad Gateway: Invalid Response From The Server", all_values)
            case 503:
                display_error("Service Unavailable: Server Is Down", all_values)
            case 504:
                display_error("Gateway timeout: No Response From The Server", all_values)
            case _:
                display_error(f"HTTP Error Occurred: {http_err}", all_values)

    except requests.exceptions.ConnectionError:
        display_error("Connection Error: Check Your Internet Connection.", all_values)

    except requests.exceptions.Timeout:
        display_error("Timeout Error: The Request Timed Out.", all_values)

    except requests.exceptions.TooManyRedirects:
        display_error("Too Many Redirects: Check The URL.", all_values)

    except requests.exceptions.RequestException as req_error:
        display_error(f"Request Error: {req_error}", all_values)
