import requests
from ipregistry import IpregistryClient

ip_registry_api_key = "7qbuqr5rnhn4az"
weather_api_key = "5954167c2589d940fb02c20fef63bc7f"
base_url = "http://api.openweathermap.org/data/2.5/weather?units=metric&appid="+weather_api_key


def my_location():
    client = IpregistryClient(ip_registry_api_key)
    result = client.lookup()
    location = result.location
    return {"lat": str(location["latitude"]), "lon": str(location["longitude"])}


def check_the_weather():
    location = my_location()
    request_url = base_url + "&lat="+location["lat"]+"&lon="+location["lon"]
    response = requests.get(request_url)
    data = response.json()
    print("log > "+str(data))

    if data["cod"] != "404":
        temperature = data["main"]["temp"]
        city = data["name"]

        answer = "It's {0} Celsius degree in {1}".format(temperature, city)
    else:
        answer = "place not found"

    return answer
