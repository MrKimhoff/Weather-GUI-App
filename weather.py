"""
Taylor Imhof
Bellevue University | DSC 510
Programming Assignment 10.1 Final Project
Created:        8/3/2021
Last Update:    8/14/2021

Change Log: [8/6/2021]  - Rearranged code so units input received before prompting city/zip code
            [8/8/2021]  - Added deg_to_cardinal() function to convert wind dir degrees to more readable format
            [8/10/2021] - Moved most of the display functionality to separate functions
                        - Cleaned up documentation
            [8/13/2021] - Fixed bug where non-numerial input would break first input() function for city/zip selection
            [8/14/2021] - Added header info; cleaned up documentation

Description: This program makes use of several concepts learned during this course. Essentially, this program allows
    the user to search for real-time weather data based on either a city or zip code received as input from the
    terminal. Using different URIs, this program attempts to make HTTP requests on data from API endpoints from
    openweathermap.org. Based on the user's selection, they will be prompted to enter either a city name, state
    abbreviation, and country code, or they will be able to look up weather data using a zip code (this method only
    works in the US). The user is also prompted for which type of units they would like displayed, as
    openweathermap.org's default temperature is Kelvin which is likely foreign to most people. Using try/except blocks
    throughout, errors are handling to continue the programs flow of execution. Using a flag variable, the program
    will also allow the user to query weather from another location until they do not wish to continue. There are a few
    functions that have been added for readability, most of which are used to display the data from weather data
    dictionary (which was created from JSON returned by the API). There is another function that simply coverts
    meteorological degrees to cardinal directions for more clarity.
"""

import requests
import json
import time


# method to convert meteorological direction in degrees to cardinal direction
def deg_to_cardinal(deg):
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    val = int((deg / 22.5) + .5)
    return dirs[val % 16]


# displays a simple header above all retrieved wx data
def display_output_header(wx_dict):
    # display header to output weather data
    display = ''.join('Current Weather For For {}'.format(wx_dict['name']))
    display_length = len(display)
    print('\n\nCurrent Weather For For {}'.format(wx_dict['name']))
    print('-' * display_length)


def display_static_wx_condition(wx_dict, temp_type, wind_speed_type):
    # display info to user via terminal
    print('Current Temp: \t\t{} {}'.format(round(wx_dict['main']['temp']), temp_type))
    print('Feels Like: \t\t{} {}'.format(round(wx_dict['main']['feels_like']), temp_type))
    print('Cloud Coverage: \t{} %'.format(wx_dict['clouds']['all']))
    print('Wind Direction: \t{}'.format(deg_to_cardinal(wx_dict['wind']['deg'])))
    print('Wind Speed: \t\t{} {}'.format(round(wx_dict['wind']['speed'], 1), wind_speed_type))


def display_dynamic_wx_conditions(wx_dict, wind_speed_type):
    if 'gust' in wx_dict['wind']:
        print('Wind Gusts: \t\t{} {}'.format(round(wx_dict['wind']['gust'], 1), wind_speed_type))
    if 'rain' in wx_dict:
        if '1h' in wx_dict['rain']:
            print('1 Hr Rain Volume: \t{} mm'.format(wx_dict['rain']['1h']))
        if '3h' in wx_dict['rain']:
            print('3 Hr Rain Volume: \t{} mm'.format(wx_dict['rain']['3h']))
        print('\nIt is currently raining! Do not forget an umbrella!')
    if 'snow' in wx_dict:
        if '1h' in wx_dict['snow']:
            print('1 Hr Snow Volume: \t{} mm'.format(wx_dict['snow']['1h']))
        if '3h' in wx_dict['snow']:
            print('3 Hr Snow Volume: \t{} mm'.format(wx_dict['snow']['3h']))
        print('\nIt is currently snowing! Here is hoping for a snow day!')


def prompt_for_retry():
    accepted_input = ['Y', 'N']
    while True:
        try:
            retry = input('Would you like to retry? [Y/N] >> ').upper()
            if retry in accepted_input:
                break
            else:
                print('Sorry, I did not understand. Please try again!')
        except ValueError:
            print('Invalid input. Please try again!')
    if retry == 'Y':
        return True
    else:
        return False


def main():
    # API key used to make HTTP request calls for wx data
    api_key = '2223f76c7bbe5b22602c8314394eb64b'

    # flag variable to control main loop execution
    another_query = 'Y'

    # display header to program
    print('Welcome to the Weather Fax application! Here, you can view realtime weather data from the US')
    print('You can query either by city or zip code')
    print('Please note that all data is retrieved from https://openweathermap.org/api\n\n')

    while another_query == 'Y':
        while True:
            print('To query weather data by "City", enter 1')
            print('To query weather data by "Zip", enter 2')
            try:
                query_type = int(input('>> '))
                if query_type in [1, 2]:
                    break
                else:
                    print('Sorry, I did not understand your input. Please try again!')
            except ValueError:
                print('Invalid input. Please try again!')

        # get type of units user would like to be displayed
        while True:
            print('Please enter the type of units you would like displayed.')
            print("Units: 'I' for Imperial; 'M' for Metric; 'S' for Standard")
            units = input('>> ').upper()
            accepted_units = ['I', 'M', 'S']
            if units in accepted_units:
                break
            else:
                print('Invalid input. Please try again!')

        # determine which unit parameter to pass into api call
        if units == 'I':
            units = 'imperial'
            temp_type = '\N{DEGREE SIGN}F'
            wind_speed_type = 'MPH'
        elif units == 'M':
            units = 'metric'
            temp_type = '\N{DEGREE SIGN}C'
            wind_speed_type = 'M/S'
        else:
            units = 'standard'
            temp_type = 'K'
            wind_speed_type = 'M/S'

        if query_type == 1:
            city = input('Enter City Name: ')
            state_code = input('Enter State Abbreviation: ')
            country_code = input('Enter Country Code: ')
            api_call = f'http://api.openweathermap.org/data/2.5/weather?q={city},{state_code},{country_code}&appid={api_key}&units={units}'
        else:
            zip_code = input('Enter Zip Code: ')
            api_call = f'http://api.openweathermap.org/data/2.5/weather?q={zip_code},US&appid={api_key}&units={units}'

        # attempt to retrieve data from api endpoint, otherwise handle error and prompt for retry
        try:
            response = requests.get(api_call)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            print('Http Error:', http_error)
            if prompt_for_retry():
                continue  # restarts program from flag var while
            else:
                print('\nSorry for not working. Hope to see you again soon!')
                break  # ends program execution
        except requests.exceptions.ConnectionError as conn_error:
            print('Connection Error:', conn_error)
            if prompt_for_retry():
                continue
            else:
                print('\nSorry for not working. Hope to see you again soon!')
                break
        except requests.exceptions.Timeout as timeout_error:
            print('Timeout Error:', timeout_error)
            if prompt_for_retry():
                continue
            else:
                print('\nSorry for not working. Hope to see you again soon!')
                break
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            if prompt_for_retry():
                continue
            else:
                print('\nSorry for not working. Hope to see you again soon!')
                break
        else:
            print('\n\nConnection successful! Now gathering weather data for your desired location. Please wait...')
            time.sleep(2)

        # store response data into a dictionary data type
        weather_data_dict = json.loads(response.text)

        # display header to output weather data
        display_output_header(weather_data_dict)

        # display static wx conditions to user via terminal
        display_static_wx_condition(weather_data_dict, temp_type, wind_speed_type)

        # display dynamic wx conditions to user via terminal
        display_dynamic_wx_conditions(weather_data_dict, wind_speed_type)

        # prompt user for another query
        while True:
            another_query = input('\n\nWould you like to look up another location\'s weather? [Y/N] >> ').upper()
            if another_query in ['Y', 'N']:
                break
            else:
                print('Invalid input. Please try again!')

        # check user selection: restart app or display thank you msg and exit app
        if another_query == 'N':
            print('\n\nThank you for using this weather application. Hope to see you again soon!')
        else:
            print('\n\nRestarting Weather Application... Please wait...')
            time.sleep(2)
            print('\n\n')


if __name__ == '__main__':
    main()
