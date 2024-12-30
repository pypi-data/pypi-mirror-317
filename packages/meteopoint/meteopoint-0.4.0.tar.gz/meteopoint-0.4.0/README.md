# MeteoPoint 🌤️

A simple CLI tool for weather and environmental data, featuring air quality monitoring with WHO guideline comparisons.

## Quick Start

```bash
# Install globally
pip install meteopoint

# Set your OpenWeather API key
export OPENWEATHER_API_KEY=your_api_key_here
export GOOGLE_MAPS_API_KEY=your_api_key_here
export GOOGLE_MAPS_SIGNING_SECRET=your_signing_secret_here

# Start using it!
meteopoint paris
meteopoint nyc
```

## Features

- 🌡️ Comprehensive weather data with beautiful display
- 💨 Air quality monitoring with WHO guideline comparisons
- 🏭 Top 5 most significant pollutants with health impact assessment
- 🌍 Enhanced accuracy with dual API support (OpenWeather + Google Maps)
- 🔄 2-day weather forecast with precipitation probability
- 🌅 Sunrise and sunset times
- 📍 Built-in city aliases (nyc, sf, etc.)

## API Keys

1. **OpenWeather API Key (Required)**
   - Sign up at [OpenWeather](https://openweathermap.org/api)
   - Free tier is sufficient
   - Set the API key as an environment variable named `OPENWEATHER_API_KEY`

2. **Google Maps API Key (Optional)**
   - Sign up at [Google Cloud Console](https://console.cloud.google.com/)
   - Enables enhanced air quality data
   - Free tier has generous limits
   - Set the API key as an environment variable named `GOOGLE_MAPS_API_KEY`
   - Set the signing secret as an environment variable named `GOOGLE_MAPS_SIGNING_SECRET`

## Examples

```bash
# Basic usage
meteopoint paris

# Use Fahrenheit
meteopoint paris --fahrenheit

# Get minimal output
meteopoint paris --format minimal

# Get JSON output
meteopoint paris --format json

# Save a city alias
meteopoint save "New York" --alias nyc

# Set default city
meteopoint config --default-city paris

# Enable shell completion
meteopoint install-completion
```

## City Aliases

Common city aliases are built-in:
- nyc → New York
- sf → San Francisco
- la → Los Angeles
- lon → London
- paris → Paris
- And many more!

## Requirements

- Python 3.7+
- Free OpenWeather API key (required)
- Free Google Maps API key (optional, enhances air quality data)

## Output Format

The tool provides rich output including:
- Current temperature and "feels like"
- Humidity and pressure
- Wind speed and direction
- Air quality index with interpretation
- Color-coded pollutant levels with WHO guideline comparisons
- Health recommendations based on air quality
- 2-day forecast with precipitation probability 