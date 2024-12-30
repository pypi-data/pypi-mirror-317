# MeteoPoint 🌤️

A beautiful CLI tool for weather and environmental data, featuring air quality monitoring with WHO guideline comparisons.

## Quick Start (2 minutes)

```bash
# Install globally
pip install meteopoint

# Run the interactive setup
meteopoint setup

# Start using it!
meteopoint paris
meteopoint nyc
```

## Features

- 🌡️ Comprehensive weather data with beautiful display
- 💨 Air quality monitoring with WHO guideline comparisons
- 🏭 Top 5 most significant pollutants with health impact assessment
- 🌍 Enhanced accuracy with dual API support
- 🔄 2-day weather forecast with precipitation probability
- 🌅 Sunrise and sunset times
- 📍 Built-in city aliases (nyc, sf, etc.)

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
- Free API key from OpenWeather (required)
- Free Google Maps API key (optional, enhances air quality data) 