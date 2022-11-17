# import libraries
from prettytable import PrettyTable
import re
import json
import pandas as pd
from textwrap import wrap
import requests

# Declared API key from OpenWeatherMap
api_key = "b87bfcc6ad1ca90766fecda4ccdff007"


# Created api_city_state function to obtain city name and state abbreviation from user input
# Validate if the city exists in multiple states
# Obtain temperature in fahrenheit
def api_city_state(cityname, stateCode):
    api_input = cityname + "," + stateCode
    api_connect = "https://api.openweathermap.org/data/2.5/weather?q={},us&" \
                  "appid={}&units=imperial".format(api_input, api_key)
    rescity = requests.get(api_connect)
    try:
        rescity.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Ooops, the following error occurred when trying to connect to WeatherMap " + str(e))
    else:
        if rescity.raise_for_status() == "200":
            print(f"Your connection to WeatherMap is successful")
    return rescity.json()


# Created api_city_state_celsius function to obtain city name and state abbreviation from user input
# Validate if the city exists in multiple states
# Obtain temperature in celsius
def api_city_state_celsius(cityname, stateCode):
    api_input = cityname + "," + stateCode
    api_connect = "https://api.openweathermap.org/data/2.5/weather?q={},us&" \
                  "appid={}&units=metric".format(api_input, api_key)
    rescity = requests.get(api_connect)
    try:
        rescity.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Ooops, the following error occurred when trying to connect to WeatherMap " + str(e))
    else:
        if requests.exceptions.HTTPError == "200":
            print(f"Your connection to WeatherMap is successful")
    return rescity.json()


# Created api_zip function to obtain zip code from user input
# Obtain temperature in fahrenheit
def api_zip(zip_code, api_key="b87bfcc6ad1ca90766fecda4ccdff007"):
    api_connect = "http://api.openweathermap.org/data/2.5/weather?zip=" \
                  + zip_code + ",us&appid=" + api_key + "&units=imperial"
    reszip = requests.get(api_connect)
    try:
        reszip.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Ooops, the following error occurred when trying to connect to WeatherMap " + str(e))
    else:
        if requests.exceptions.HTTPError == "200":
            print(f"Your connection to WeatherMap is successful")
    return reszip.json()


# Created api_zip_celsius function to obtain zip code from user input
# Obtain temperature in celsius
def api_zip_celsius(zip_code, api_key="b87bfcc6ad1ca90766fecda4ccdff007"):
    api_connect = "http://api.openweathermap.org/data/2.5/weather?zip=" \
                  + zip_code + ",us&appid=" + api_key + "&units=metric"
    reszip = requests.get(api_connect)
    try:
        reszip.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Ooops, the following error occurred when trying to connect to WeatherMap " + str(e))
    else:
        if requests.exceptions.HTTPError == "200":
            print(f"Your connection to WeatherMap is successful")
    return reszip.json()


# Created api_city function to obtain city name from user
# Obtain temperature in fahrenheit
def api_city(cityname, api_key="b87bfcc6ad1ca90766fecda4ccdff007"):
    api_connect = "http://api.openweathermap.org/data/2.5/weather?q=" \
                  + cityname + ",us&appid=" + api_key + "&units=imperial"
    rescity = requests.get(api_connect)
    try:
        rescity.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Ooops, the following error occurred when trying to connect to WeatherMap " + str(e))
    else:
        if requests.exceptions.HTTPError == "200":
            print(f"Your connection to WeatherMap is successful")
    return rescity.json()


# Created api_city_celsius function to obtain city name from user
# Obtain temperature in celsius
def api_city_celsius(cityname, api_key="b87bfcc6ad1ca90766fecda4ccdff007"):
    api_connect = "http://api.openweathermap.org/data/2.5/weather?q=" \
                  + cityname + ",us&appid=" + api_key + "&units=metric"
    rescity = requests.get(api_connect)
    try:
        rescity.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Ooops, the following error occurred when trying to connect to WeatherMap " + str(e))
    else:
        if requests.exceptions.HTTPError == "200":
            print(f"Your connection to WeatherMap is successful")
    return rescity.json()


# Created json_dict_output function to print output
# Used json.loads to convert the string into a dictionary
def json_dict_output(obj):
    text = json.dumps(obj, sort_keys=True, indent=15)
    resp = json.loads(text)

    # Created a new dictionary
    jsn_dict = {}
    try:
        print("\n")
        jsn_dict["Name"] = resp["name"]
        jsn_dict["Country"] = resp["sys"]["country"]
        jsn_dict["Current Conditions"] = resp["weather"][0]["description"].title()
        jsn_dict["Current Temperature"] = str(resp["main"]["temp"]) + "°"
        jsn_dict["Recorded High Temp"] = str(resp["main"]["temp_max"]) + "°"
        jsn_dict["Recorded Low Temp"] = str(resp["main"]["temp_min"]) + "°"
        jsn_dict["Feels like"] = str(resp["main"]["feels_like"]) + "°"
        jsn_dict["Wind Speed"] = str(resp["wind"]["speed"]) + " mph"
        jsn_dict["Pressure"] = str(resp["main"]["pressure"]) + " hPa"
        jsn_dict["Visibility"] = str(resp["visibility"]) + " m"
        jsn_dict["Humidity"] = str(resp["main"]["humidity"]) + "%"

        # Using pretty print for formatting
        tab = PrettyTable(["Weather Information", "Details"])
        for key, val in jsn_dict.items():
            wrapped_value_lines = wrap(str(val) or "", 60) or [""]
            tab.add_row([key, wrapped_value_lines[0]])
            for subseq in wrapped_value_lines[1:]:
                tab.add_row(["", subseq])
        print(tab)
    # Created error message in the event user inputs an invalid entry
    except:
        print("The city name entered, cannot be found in the database!")
        print()


# Created city_database function to obtain raw database file for all cities from WeatherMap
# city_database function converts Json output to panda
def city_database():
    url = "http://bulk.openweathermap.org/sample/city.list.json.gz"
    data_frame = pd.read_json(url)
    return data_frame


# Created validate_city function to associate all state codes to the city input
def validate_city(city):
    data_frame = city_database()
    state_codes_by_city = data_frame.loc[
        (data_frame["name"] == city) & (data_frame["country"] == "US"), ["state"]].values.tolist()
    count_state = len(state_codes_by_city)
    state_codes = {}
    state_codes["steCount"] = count_state
    state_codes["State_Name"] = state_codes_by_city
    state_codes["City"] = city
    return state_codes


# Created check_city_state function to validate association between city and state
# Function will display list of all state codes that contain the same city input from user
def check_city_state(city_name, state_code):
    data_frame = city_database()
    lookup_location = data_frame.loc[
        (data_frame["name"] == city_name) & (data_frame["state"] == state_code) & (data_frame["country"] == "US"),
        ["id", "name", "state", "country", "coord"]]
    if len(lookup_location) == 1:
        longitude = lookup_location.coord.str["lon"].iloc[0]
        latitude = lookup_location.coord.str["lat"].iloc[0]
        city = str(lookup_location["name"].iloc[0]).strip()
        state_code = str(lookup_location["state"].iloc[0]).strip()
        city_state = (city + ", " + state_code)
    return city, state_code


# Created check_zip_code function to ensure user input a valid zip code
def check_zip_code(zip_code):
    return re.match(r"\b\d{5}\b", zip_code)  # found this on the internet...


# Created option function to display options and obtain input from user
def option():
    print(f"Please input the number (0-4) of the search you would like to complete")
    print(f"1 - Search Zip Code in fahrenheit")
    print(f"2 - Search City in fahrenheit")
    print(f"3 - Search Zip Code in celsius")
    print(f"4 - Search City in celsius")
    print(f"0 - Exit the WeatherMap program")
    print("\n")
    return input(f"Which search would you like to complete today: ")


# Created main function to obtain user input
def main(api_key="b87bfcc6ad1ca90766fecda4ccdff007"):
    print("\n")
    print(f"Thank you for choosing WeatherMap app for your weather needs")
    print("\n")
    # Created while loop
    while True:
        choice = option()
        while True:
            if choice == "1":
                input_zip = input(f"Please enter the zip code you wish to search today: ").strip().lower()
                print("\n")
                correct_zip = check_zip_code(input_zip)
                if correct_zip:
                    print("\n")
                    json_dict_output(api_zip(input_zip, api_key))
                    break
                else:
                    print(f"Your entry is not valid. Please enter a valid five digit zip code: ")
                    continue

            elif choice == "3":
                input_zip_cel = input(f"Please enter the zip code you wish to search today: ").strip().lower()
                print("\n")
                correct_zip = check_zip_code(input_zip_cel)
                if correct_zip:
                    print("\n")
                    json_dict_output(api_zip_celsius(input_zip_cel, api_key))
                    break
                else:
                    print(f"Your entry is not valid. Please enter a valid five digit zip code: ")
                    continue

            # Accounting for cities found in multiple states
            elif choice == "4":
                city_name_cel = input(f"Please enter the name of the city you wish to search today: ").strip().title()
                print("\n")
                validation_lookup = validate_city(city_name_cel)
                if validation_lookup["steCount"] > 1:
                    while True:
                        print("\n")
                        print("The city you entered exists in the following " + str(
                            validation_lookup["steCount"]) + " states: ")
                        print(", ".join(" ".join(map(str, state)) for state in validation_lookup["State_Name"]))
                        state_code = input(f"Enter a state abbreviation, for the city you would like to search: "
                                           ).strip().upper()
                        try:
                            city, state_code = check_city_state(city_name_cel, state_code)
                        except:
                            print(f"That state does not match a city. Please choose a value from the list provided")
                            print("\n")
                            continue
                        else:
                            print("\n")
                            print("Weather in " + city_name_cel + "," + str(state_code))
                            json_dict_output(api_city_state_celsius(city, state_code))
                            break
                elif validation_lookup["steCount"] == 1:
                    state_code = validation_lookup["State_Name"][0][0]
                    print("\n")
                    print(city_name_cel + " exists in: " + str(state_code))
                    print("\n")
                    print("Weather in " + city_name_cel + "," + str(state_code))
                    json_dict_output(api_city_celsius(city_name_cel, api_key))
                else:
                    print(f"The city you entered was not found by WeatherMap")
                break

            # Force user to provide a state code when city is listed in multiple states
            elif choice == "2":
                city_name = input(f"Please enter the name of the city you wish to search today: ").strip().title()
                print("\n")
                validation_lookup = validate_city(city_name)

                if validation_lookup["steCount"] > 1:
                    while True:
                        print("\n")
                        print(f"The city you entered is located in the following " + str(
                            validation_lookup["steCount"]) + " states: ")
                        print(", ".join(" ".join(map(str, state)) for state in validation_lookup["State_Name"]))
                        state_code = input(f"Enter the state abbreviation, for the city you are looking up: "
                                           ).strip().upper()

                        try:
                            city, state_code = check_city_state(city_name, state_code)
                        except:
                            print(f"That state does not match a city. Please choose a value from the list provided")
                            print("\n")
                            continue
                        else:
                            print("\n")
                            print(f"Weather in " + city_name + "," + str(state_code))
                            json_dict_output(api_city_state(city, state_code))
                            break

                # Validate if the city is listed in more than one state
                elif validation_lookup["steCount"] == 1:
                    state_code = validation_lookup["State_Name"][0][0]
                    print("\n")
                    print(city_name + " exists in: " + str(state_code))
                    print("\n")
                    print(f"Weather in " + city_name + "," + str(state_code))
                    Json_dict_output(apiCity(city_name, api_key))
                else:
                    print(f"\nThe city you entered was not found by WeatherMap.")
                    print("\n")
                break

            # Allow user the option to exit the program
            elif choice == "0":
                print("\n")
                print(f"Thank you for using WeatherMap for all of your weather needs.")
                exit()
            else:
                print("\n")
                print(f"That is an invalid entry, please try again")
                break


if __name__ == "__main__":
    main()
