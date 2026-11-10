import argparse
import json
import os
import sys
import time
import requests

CACHE_FILE = "weather_cache.json"
CACHE_DURATION = 1800

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

def get_coordinates(city):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    try:
        response = requests.get(geo_url, timeout=10)
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            loc = data["results"][0]
            return loc["latitude"], loc["longitude"], loc["name"], loc.get("country", "")
    except Exception as e:
        print(f"Error connecting to geocoding service: {e}")
    return None, None, None, None

def get_weather(city, use_cache=True):
    city_key = city.lower().strip()
    cache = load_cache()
    current_time = time.time()

    if use_cache and city_key in cache:
        cached_data = cache[city_key]
        if current_time - cached_data["timestamp"] < CACHE_DURATION:
            print("[INFO] Serving weather data from local cache...")
            return cached_data["data"]

    print(f"[INFO] Fetching fresh weather data for '{city}'...")
    lat, lon, city_name, country = get_coordinates(city)
    if lat is None:
        print(f"Error: City '{city}' could not be found.")
        sys.exit(1)

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature"
    
    try:
        response = requests.get(weather_url, timeout=10)
        if response.status_code != 200:
            print(f"Error: Failed to fetch weather data (Status code: {response.status_code})")
            sys.exit(1)
        
        data = response.json()
        current = data.get("current", {})
        
        weather_info = {
            "city": city_name,
            "country": country,
            "temperature": current.get("temperature_2m"),
            "feels_like": current.get("apparent_temperature"),
            "humidity": current.get("relative_humidity_2m"),
            "unit": data.get("current_units", {}).get("temperature_2m", "°C")
        }

        cache[city_key] = {
            "timestamp": current_time,
            "data": weather_info
        }
        save_cache(cache)

        return weather_info

    except Exception as e:
        print(f"Error connecting to weather service: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Weather API Wrapper Service CLI")
    parser.add_argument("city", type=str, help="Name of the city to query weather for")
    parser.add_argument("--no-cache", action="store_true", help="Bypass the cache and fetch live data")

    args = parser.parse_args()

    weather = get_weather(args.city, use_cache=not args.no_cache)

    print("\n" + "=" * 42)
    print(f"  WEATHER REPORT: {weather['city']}, {weather['country']}")
    print("=" * 42)
    print(f"  Temperature : {weather['temperature']}{weather['unit']}")
    print(f"  Feels Like  : {weather['feels_like']}{weather['unit']}")
    print(f"  Humidity    : {weather['humidity']}%")
    print("=" * 42)

if __name__ == "__main__":
    main()