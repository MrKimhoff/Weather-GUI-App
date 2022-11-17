import tkinter as tk
import requests
import time


def get_weather(canvas):
    city = textfield.get()
    api_key = "2223f76c7bbe5b22602c8314394eb64b"
    api = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api_key
    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)
    temp_min = int(json_data['main']['temp_min'] - 273.15)
    temp_max = int(json_data['main']['temp_max'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']
    sunrise = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunrise'] - 21600))
    sunset = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunset'] - 21600))

    final_info = condition + '\n' + str(temp) + 'Celsius'
    final_data = '\n' + 'Max Temp: ' + str(temp_max) + '\n' + 'Min Temp: ' + str(temp_min) + '\n' 'Pressure: ' + str(
        pressure) + '\n' + 'Humidity: ' + str(humidity) + '\n' + 'Wind Speed: ' + str(
        wind) + '\n' 'Sunrise: ' + sunrise + '\n' + 'Sunset: ' + sunset

    label1.config(text=final_info)
    label2.config(text=final_data)


canvas = tk.Tk()
canvas.geometry("600x500")
canvas.title("Weather App")

f = ('poppins', 15, 'bold')
t = ('poppins', 35, 'bold')

textfield = tk.Entry(canvas, font=t)
textfield.pack(pady=20)
textfield.focus()
textfield.bind('<Return>', get_weather)

label1 = tk.Label(canvas, font=t)
label1.pack()

label2 = tk.Label(canvas, font=f)
label2.pack()

canvas.mainloop()

