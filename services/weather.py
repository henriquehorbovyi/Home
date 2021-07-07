import random

import requests
from ipregistry import IpregistryClient

ip_registry_api_key = "7qbuqr5rnhn4az"
weather_api_key = "5954167c2589d940fb02c20fef63bc7f"
base_url = "http://api.openweathermap.org/data/2.5/weather?units=metric&appid=" + weather_api_key
initial_phrase = ['currently', 'right now', 'now']


def my_location():
    client = IpregistryClient(ip_registry_api_key)
    result = client.lookup()
    location = result.location
    return {"lat": str(location["latitude"]), "lon": str(location["longitude"])}


def check_the_weather(city=''):
    request_url = base_url

    if city == '':
        location = my_location()
        request_url = request_url + "&lat=" + location["lat"] + "&lon=" + location["lon"]
    else:
        request_url = request_url + "&q=" + city

    response = requests.get(request_url)
    data = response.json()
    print("log > " + str(data))
    if data["cod"] != "404":
        city = data["name"]
        temperature = int(data["main"]["temp"])
        min_temperature = int(data['main']['temp_min'])
        max_temperature = int(data['main']['temp_max'])

        answer = "{0} in {1} it's {2} degrees, with the forecast high of {3} and the low of {4}".format(
            random.choice(initial_phrase), city, temperature, max_temperature, min_temperature)
    else:
        answer = "place not found"

    return answer
