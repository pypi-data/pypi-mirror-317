# MeteoPoint 🌤️

A beautiful CLI tool for weather and environmental data.

## Quick Start (2 minutes setup)

```bash
# 1. Install with pip
pip install meteopoint

# 2. Run the setup guide
meteopoint setup

# 3. Start using it!
meteopoint paris
meteopoint nyc
```

## API Keys Setup

MeteoPoint works with either one or both of these free API keys:

### Basic Setup (Good) - OpenWeather API only
1. Sign up at https://openweathermap.org/
2. Copy your API key
3. Set it in your terminal:
```bash
export OPENWEATHER_API_KEY=your_key_here
```

### Enhanced Setup (Best) - Both APIs
1. Complete the Basic Setup above
2. Get Google Maps API key:
   - Go to https://console.cloud.google.com/
   - Enable Air Quality API
   - Create API key and signing secret
3. Set the additional keys:
```bash
export GOOGLE_MAPS_API_KEY=your_key_here
export GOOGLE_MAPS_SIGNING_SECRET=your_secret_here
```

💡 **Tip**: To make the API keys permanent, add the export lines to your `~/.bashrc` or `~/.zshrc`

## Features

- Current weather conditions with beautiful emoji ☀️ 🌧️ ⛈️
- Air quality data and pollutant levels
  - Enhanced accuracy with both APIs
  - Fallback to OpenWeather data when using single API
- 2-day weather forecast
- Temperature, humidity, wind, and pressure
- Sunrise and sunset times
- Built-in city aliases (nyc, sf, etc.)

## Examples

```bash
# Basic usage
meteopoint paris

# Use Fahrenheit instead of Celsius
meteopoint paris --fahrenheit

# Get minimal output
meteopoint paris --format minimal

# Get JSON output for scripting
meteopoint paris --format json

# Save a city with an alias
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
- OpenWeather API key (free, required)
- Google Maps API key (free, optional but recommended) 