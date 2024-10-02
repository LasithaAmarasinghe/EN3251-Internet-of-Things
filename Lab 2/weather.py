import requests

# Your OpenWeather API key (replace with your actual key)
api_key = "d77718b52619d73c26d0cb1f2e3ef25e"

for i in range(5):
    # City for which you want weather data
    city = input("Enter the city:")

    # API URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    # Send a GET request to the API
    response = requests.get(url)

    # Parse the JSON response
    weather_data = response.json()

    # Check if the response is valid
    if response.status_code == 200:
        # Print city and weather information
        print(f"City: {weather_data['name']}")
        print(f"Temperature: {weather_data['main']['temp']} C")
        print(f"Weather: {weather_data['weather'][0]['description']}")
        print(f"Humidity: {weather_data['main']['humidity']}%")
        print(f"Wind Speed: {weather_data['wind']['speed']} m/s")
        print( )

    else:
        print(f"Error fetching weather data: {weather_data.get('message', 'Unknown error')}")