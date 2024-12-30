# MeteoPoint 🌤️

A simple CLI tool for weather and environmental data, featuring air quality monitoring with WHO guideline comparisons.

## Quick Start (2 minutes)

```bash
# Install globally
pip install meteopoint

# Run the interactive setup (you'll need an OpenWeather API key)
meteopoint setup

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

2. **Google Maps API Key (Optional)**
   - Sign up at [Google Cloud Console](https://console.cloud.google.com/)
   - Enables enhanced air quality data
   - Free tier has generous limits

The `meteopoint setup` command will guide you through the process.

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