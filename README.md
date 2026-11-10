# Weather API Wrapper Service

This project is my completed solution for the Roadmap.sh challenge: Weather API Wrapper Service.

Challenge URL: https://roadmap.sh/projects/weather-api-wrapper-service

## Overview

This is a simple Python command-line app that fetches the current weather for a city by combining public weather and geocoding APIs. It is designed to be easy to use, lightweight, and practical for everyday local weather checks.

The application:
- looks up a city using the Open-Meteo geocoding API
- fetches live weather data for that location
- displays temperature, feels-like temperature, and humidity
- caches recent results locally to reduce repeated API calls
- supports an option to bypass the cache for fresh data

## Why this project exists

The goal of this challenge is to build a small API wrapper service that interacts with real weather data providers and presents clean, useful output to the user. This project demonstrates how to:
- call external APIs from Python
- handle JSON responses
- store local cache files
- build a CLI tool with a friendly user experience

## Features

- City-based weather lookup
- Live weather data from Open-Meteo
- Local JSON cache for faster repeated requests
- Cache expiration window to refresh data automatically
- Command-line usage for quick checks

## Project structure

- `main.py` – main CLI logic
- `weather_cache.json` – local cache file generated during use
- `requirements.txt` – Python dependencies

## Requirements

- Python 3.x
- Internet access to reach the weather APIs
- `requests` package

## Installation

1. Open a terminal in the project folder.
2. Create and activate a virtual environment if you want an isolated setup:

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

3. Install project dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Fetch the current weather for a city:

```bash
python main.py "London"
```

Force a fresh API request without using the cache:

```bash
python main.py "London" --no-cache
```

Example output:

```text
WEATHER REPORT: London, United Kingdom
Temperature : 18.2°C
Feels Like  : 17.8°C
Humidity    : 64%
```

## How caching works

The app stores weather results in `weather_cache.json` and keeps each city's weather data for a set time period. If data is still fresh, the app serves it from the cache instead of calling the API again.

This helps reduce repeated requests while still allowing users to skip the cache when they need the newest weather information.

## Notes

This project is a lightweight weather wrapper built for learning and demonstration. It is intentionally simple and focused on the challenge requirements rather than production-level scaling or a full web service.

## Challenge completion

This repository was created to complete the Roadmap.sh Weather API Wrapper Service challenge and demonstrates a working Python implementation of the requested functionality.
