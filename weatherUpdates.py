import pandas as pd
import requests, json, datetime
from plyer import notification

lat=38.3357
lon=-77.4342
part="minutely"
APIkey="56917cc227986aeab113d819b96220ab"

url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={APIkey}'

querystring = {"units":"imperial"}

response = requests.request("GET", url, params = querystring)

weather_dict = json.loads(response.text)

def get_alerts():
    if 'alerts' not in weather_dict.keys():
        alerts = "No weather alerts"
        return alerts
    else:
        alerts = []
        for i in weather_dict['alerts']:
            alerts.append(i['event'])
        for i in alerts:
            return i

current_time = datetime.datetime.fromtimestamp(weather_dict['current']['dt']).time()    
sunset = datetime.datetime.fromtimestamp(weather_dict['current']['sunset'])
sunset = sunset.time()
desc = weather_dict['current']['weather'][0]['description']
temp = weather_dict['current']['temp']
#icon = weather_dict['current']['weather'][0]['icon']
alerts = get_alerts()

notification.notify(title = "Weather Update", 
                    message = f"Now: {current_time} \nIt is currently {temp} deg F and {desc}\nThe sun will set at approximately {sunset}\n{alerts}", 
                    timeout=10)