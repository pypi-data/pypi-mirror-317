#!/usr/bin/env python3

import os
import sys
import json
import typer
import hmac
import base64
import hashlib
import requests
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv
from meteopoint.config import Config

# Load environment variables and config
load_dotenv()
config = Config()
app = typer.Typer(help="MeteoPoint - A beautiful weather CLI")
console = Console()

# API Keys
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
GOOGLE_MAPS_SIGNING_SECRET = os.getenv("GOOGLE_MAPS_SIGNING_SECRET")

def sign_url(url: str, secret: str) -> str:
    """Sign a URL using the Google Maps signing secret"""
    if not secret:
        return url
    
    url_to_sign = url.split('?')[1].encode()
    decoded_key = base64.b64decode(secret.encode())
    signature = hmac.new(decoded_key, url_to_sign, hashlib.sha1)
    encoded_signature = base64.b64encode(signature.digest()).decode()
    return f"{url}&signature={encoded_signature}"

def get_weather_data(city: str):
    """Fetch weather data for a given city"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        console.print(f"[red]Error fetching weather data: {str(e)}")
        sys.exit(1)

def get_air_quality(lat: float, lon: float):
    """Fetch air quality data using Google Maps Air Quality API with OpenWeather fallback"""
    # Try Google Maps Air Quality API first
    base_url = "https://airquality.googleapis.com/v1/currentConditions:lookup"
    
    request_body = {
        "location": {
            "latitude": lat,
            "longitude": lon
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY
    }
    
    try:
        response = requests.post(
            base_url,
            json=request_body,
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        
        # Always get detailed pollutant data from OpenWeather
        ow_base_url = "http://api.openweathermap.org/data/2.5/air_pollution"
        ow_params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY
        }
        
        try:
            ow_response = requests.get(ow_base_url, params=ow_params)
            ow_response.raise_for_status()
            return {
                "source": "google",
                "data": data,
                "pollutants": ow_response.json()
            }
        except requests.RequestException:
            return {"source": "google", "data": data}
            
    except requests.RequestException as e:
        # Fallback to OpenWeather Air Pollution API
        base_url = "http://api.openweathermap.org/data/2.5/air_pollution"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return {"source": "openweather", "data": response.json()}
        except requests.RequestException as e:
            console.print(f"[red]Error fetching air quality data: {str(e)}")
            return None

def get_who_guidelines():
    """Return WHO guidelines for pollutants"""
    return {
        "PM2.5": {"value": 10, "unit": "µg/m³"},  # Annual mean
        "PM10": {"value": 20, "unit": "µg/m³"},   # Annual mean
        "NO2": {"value": 40, "unit": "µg/m³"},    # Annual mean
        "O3": {"value": 100, "unit": "µg/m³"},    # 8-hour mean
        "SO2": {"value": 40, "unit": "µg/m³"},    # 24-hour mean
        "CO": {"value": 4, "unit": "mg/m³"},      # 24-hour mean
    }

def get_pollutant_health_impact(pollutant: str, value: float) -> tuple:
    """Get health impact level and color for a pollutant"""
    guidelines = get_who_guidelines()
    if pollutant not in guidelines:
        return "Unknown", "white"
    
    guideline = guidelines[pollutant]["value"]
    ratio = value / guideline
    
    if ratio <= 0.5:
        return "Safe", "green"
    elif ratio <= 1.0:
        return "Acceptable", "green"
    elif ratio <= 2.0:
        return "Moderate", "yellow"
    elif ratio <= 3.5:
        return "High", "red"
    else:
        return "Very High", "red"

def get_aqi_interpretation(aqi: float) -> str:
    """Get detailed AQI interpretation"""
    if aqi <= 25:
        return "[green]Excellent - Perfect for outdoor activities[/green]"
    elif aqi <= 50:
        return "[green]Good - Air quality is satisfactory[/green]"
    elif aqi <= 75:
        return "[yellow]Moderate - May affect sensitive individuals[/yellow]"
    elif aqi <= 100:
        return "[yellow]Fair - Sensitive groups may experience effects[/yellow]"
    elif aqi <= 150:
        return "[red]Poor - Everyone may experience health effects[/red]"
    else:
        return "[red]Very Poor - Avoid outdoor activities[/red]"

def format_pollutant_display(pollutants: dict) -> str:
    """Format pollutant display with color coding and WHO comparisons"""
    if not pollutants:
        return "No pollutant data available"
    
    # Calculate health impact for each pollutant
    pollutant_impacts = {}
    for name, data in pollutants.items():
        if name in get_who_guidelines():
            impact, color = get_pollutant_health_impact(name, data["value"])
            pollutant_impacts[name] = {
                "value": data["value"],
                "unit": data["unit"],
                "impact": impact,
                "color": color,
                "ratio": data["value"] / get_who_guidelines()[name]["value"]
            }
    
    # Sort by impact ratio and take top 5
    sorted_pollutants = sorted(
        pollutant_impacts.items(),
        key=lambda x: x[1]["ratio"],
        reverse=True
    )[:5]
    
    # Format the display
    lines = []
    for name, data in sorted_pollutants:
        color = data["color"]
        lines.append(
            f"• {name}: [{color}]{data['value']} {data['unit']} - {data['impact']}[/{color}]"
        )
    
    return "\n".join(lines)

def get_aqi_from_response(aqi_data: dict) -> tuple:
    """Extract AQI information from either Google or OpenWeather response"""
    if not aqi_data:
        return None, None, None, None, {}
    
    source = aqi_data["source"]
    data = aqi_data["data"]
    pollutants = {}
    
    # Get pollutant data from OpenWeather if available
    if source == "openweather" and "list" in data and data["list"]:
        components = data["list"][0]["components"]
        # Map component names to more readable format
        component_map = {
            "co": "CO",
            "no": "NO",
            "no2": "NO2",
            "o3": "O3",
            "so2": "SO2",
            "pm2_5": "PM2.5",
            "pm10": "PM10",
            "nh3": "NH3"
        }
        
        # Get all pollutant concentrations
        for code, value in components.items():
            if code in component_map:
                unit = "µg/m³" if code not in ["co"] else "mg/m³"
                pollutants[component_map[code]] = {
                    "value": value,
                    "unit": unit,
                    "display": f"{value} {unit}"
                }
    elif "pollutants" in aqi_data:
        components = aqi_data["pollutants"]["list"][0]["components"]
        # Map component names to more readable format
        component_map = {
            "co": "CO",
            "no": "NO",
            "no2": "NO2",
            "o3": "O3",
            "so2": "SO2",
            "pm2_5": "PM2.5",
            "pm10": "PM10",
            "nh3": "NH8"
        }
        
        # Get all pollutant concentrations
        for code, value in components.items():
            if code in component_map:
                unit = "µg/m³" if code not in ["co"] else "mg/m³"
                pollutants[component_map[code]] = {
                    "value": value,
                    "unit": unit,
                    "display": f"{value} {unit}"
                }
    
    if source == "google":
        if "indexes" in data:
            for index in data.get("indexes", []):
                if index.get("code") == "uaqi":
                    return (
                        index.get("aqi"),
                        index.get("category"),
                        index.get("dominantPollutant", "").upper(),
                        data.get("dateTime"),
                        pollutants
                    )
    elif source == "openweather":
        if "list" in data and data["list"]:
            aqi_level = data["list"][0]["main"]["aqi"]
            components = data["list"][0]["components"]
            
            # Get dominant pollutant (highest concentration relative to standard)
            dominant_pollutant = max(components.items(), key=lambda x: x[1])[0].upper()
            
            # Map OpenWeather AQI levels (1-5) to a 0-100 scale
            categories = {
                1: "Good air quality",
                2: "Fair air quality",
                3: "Moderate air quality",
                4: "Poor air quality",
                5: "Very poor air quality"
            }
            
            # Convert 1-5 scale to 0-100 scale
            aqi_value = ((aqi_level - 1) * 25)  # This maps 1->0, 2->25, 3->50, 4->75, 5->100
            
            return (
                aqi_value,
                categories.get(aqi_level, "Unknown"),
                dominant_pollutant,
                data["list"][0].get("dt"),
                pollutants
            )
    
    return None, None, None, None, {}

def get_forecast(lat: float, lon: float):
    """Fetch 2-day weather forecast"""
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "cnt": 16  # Limit to next 2 days (8 measurements per day)
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        console.print(f"[red]Error fetching forecast data: {str(e)}")
        return None

def get_weather_emoji(code: int) -> str:
    """Get appropriate weather emoji based on condition code"""
    if code == 800:  # Clear sky
        return "☀️"
    elif code == 801:  # Few clouds
        return "🌤️"
    elif code in [802, 803]:  # Scattered/broken clouds
        return "⛅"
    elif code == 804:  # Overcast clouds
        return "☁️"
    elif code >= 200 and code < 300:  # Thunderstorm
        return "⛈️"
    elif code >= 300 and code < 400:  # Drizzle
        return "🌧️"
    elif code >= 500 and code < 600:  # Rain
        return "🌧️"
    elif code >= 600 and code < 700:  # Snow
        return "🌨️"
    elif code >= 700 and code < 800:  # Atmosphere (fog, mist, etc)
        return "🌫️"
    return "🌡️"

def get_wind_direction(degrees: float) -> str:
    """Convert wind degrees to cardinal direction"""
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                 "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / (360 / len(directions))) % len(directions)
    return directions[index]

def format_time(timestamp: int, timezone_offset: int) -> str:
    """Format Unix timestamp to local time string"""
    from datetime import datetime
    local_time = datetime.utcfromtimestamp(timestamp + timezone_offset)
    return local_time.strftime("%H:%M")

def get_cities_completion():
    """Get completion list for cities"""
    return config.get_all_aliases()

def setup_api_keys():
    """Interactive setup for API keys"""
    console.print("\n[bold blue]Thank you for using MeteoPoint![/bold blue]")
    console.print("\n1. First, let's set up your OpenWeather API key (required)")
    console.print("   Get it from: [link]https://openweathermap.org/[/link]")
    
    openweather_key = os.getenv("OPENWEATHER_API_KEY")
    if not openweather_key:
        console.print("\nEnter your OpenWeather API key:")
        openweather_key = input("> ").strip()
        if not openweather_key:
            console.print("[red]Error: OpenWeather API key is required[/red]")
            return
    else:
        console.print(f"[green]✓ OpenWeather API key found in environment[/green]")
        use_existing = input("Would you like to keep using this key? (Y/n): ").strip().lower()
        if use_existing == 'n':
            console.print("\nEnter your new OpenWeather API key:")
            openweather_key = input("> ").strip()
            if not openweather_key:
                console.print("[red]Error: OpenWeather API key is required[/red]")
                return
    
    console.print("\n2. Would you like to set up Google Maps API for enhanced air quality data? (optional)")
    console.print("   Get it from: [link]https://console.cloud.google.com/[/link]")
    setup_google = input("Set up Google Maps API? (y/N): ").strip().lower() == 'y'
    
    google_key = os.getenv("GOOGLE_MAPS_API_KEY")
    google_secret = os.getenv("GOOGLE_MAPS_SIGNING_SECRET")
    
    if setup_google:
        if google_key and google_secret:
            console.print("[green]✓ Google Maps API keys found in environment[/green]")
            use_existing = input("Would you like to keep using these keys? (Y/n): ").strip().lower()
            if use_existing == 'n':
                console.print("\nEnter your new Google Maps API key:")
                google_key = input("> ").strip()
                console.print("\nEnter your new Google Maps Signing Secret:")
                google_secret = input("> ").strip()
        else:
            console.print("\nEnter your Google Maps API key:")
            google_key = input("> ").strip()
            console.print("\nEnter your Google Maps Signing Secret:")
            google_secret = input("> ").strip()
    
    # Save to .env file
    env_path = os.path.expanduser("~/.meteopoint.env")
    with open(env_path, "w") as f:
        f.write(f"OPENWEATHER_API_KEY={openweather_key}\n")
        if setup_google and google_key and google_secret:
            f.write(f"GOOGLE_MAPS_API_KEY={google_key}\n")
            f.write(f"GOOGLE_MAPS_SIGNING_SECRET={google_secret}\n")
    
    os.chmod(env_path, 0o600)  # Set file permissions to user read/write only
    
    # Add to shell config if requested
    shell_config = os.path.expanduser("~/.zshrc" if os.getenv("SHELL", "").endswith("zsh") else "~/.bashrc")
    console.print(f"\nWould you like to add the API keys to your shell config ({shell_config})?")
    add_to_shell = input("This will make them permanent (y/N): ").strip().lower() == 'y'
    
    if add_to_shell:
        with open(shell_config, "a") as f:
            f.write(f"\n# MeteoPoint API keys\n")
            f.write(f'export OPENWEATHER_API_KEY="{openweather_key}"\n')
            if setup_google and google_key and google_secret:
                f.write(f'export GOOGLE_MAPS_API_KEY="{google_key}"\n')
                f.write(f'export GOOGLE_MAPS_SIGNING_SECRET="{google_secret}"\n')
        console.print(f"[green]✓ API keys added to {shell_config}[/green]")
        console.print(f"[yellow]Please run: source {shell_config}[/yellow]")
    else:
        # Set environment variables for immediate use
        os.environ["OPENWEATHER_API_KEY"] = openweather_key
        if setup_google and google_key and google_secret:
            os.environ["GOOGLE_MAPS_API_KEY"] = google_key
            os.environ["GOOGLE_MAPS_SIGNING_SECRET"] = google_secret
    
    console.print("\n[bold green]Setup complete! Try running:[/bold green]")
    console.print("meteopoint paris")

@app.command()
def setup():
    """Set up API keys for MeteoPoint"""
    setup_api_keys()

@app.callback(invoke_without_command=True)
def main(
    city: str = typer.Argument(
        None,
        help="City name or alias",
        autocompletion=get_cities_completion
    ),
    format: str = typer.Option(
        None,
        "--format", "-f",
        help="Output format (pretty/json/minimal)",
        autocompletion=lambda: ["pretty", "json", "minimal"]
    ),
    fahrenheit: bool = typer.Option(
        False,
        "--fahrenheit",
        help="Show temperature in Fahrenheit"
    )
):
    """
    Get weather and environmental data for a specified city
    """
    # Skip API key check if running setup command
    ctx = typer.get_current_context()
    if ctx.invoked_subcommand == "setup":
        return

    if not city and not ctx.invoked_subcommand:
        # If no city and no subcommand, use default city
        city = config.get_default_city()
        if not city:
            console.print("[red]Error: No city specified and no default city set[/red]")
            return
    elif not city:
        # If no city but subcommand exists, just return
        return

    if not OPENWEATHER_API_KEY:
        console.print("[red]Error: OPENWEATHER_API_KEY environment variable is not set")
        console.print("[yellow]Run 'meteopoint setup' to configure your API keys[/yellow]")
        sys.exit(1)

    # Resolve city alias if it exists
    resolved_city = config.get_city(city)
    if resolved_city:
        city = resolved_city

    # Get output format
    output_format = format or config.get_format()
    
    # Get temperature unit
    use_fahrenheit = fahrenheit or config.get_temperature_unit() == "fahrenheit"

    try:
        # Fetch weather data
        weather_data = get_weather_data(city)
        
        # Get coordinates for air quality data
        lat = weather_data["coord"]["lat"]
        lon = weather_data["coord"]["lon"]
        
        # Fetch air quality and forecast data
        aqi_data = get_air_quality(lat, lon)
        forecast_data = get_forecast(lat, lon)
        
        # Extract AQI information
        aqi_value, aqi_category, dominant_pollutant, last_updated, pollutants = get_aqi_from_response(aqi_data)
        
        # Prepare the display
        temp = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        city_name = f"{weather_data['name']}, {weather_data['sys']['country']}"
        
        # Convert temperature if needed
        if use_fahrenheit:
            temp = (temp * 9/5) + 32
            feels_like = (feels_like * 9/5) + 32
            temp_unit = "°F"
        else:
            temp_unit = "°C"
        
        # Get weather emoji
        weather_code = weather_data["weather"][0]["id"]
        weather_emoji = get_weather_emoji(weather_code)
        
        # Format wind data
        wind_speed = weather_data["wind"]["speed"]
        wind_direction = get_wind_direction(weather_data["wind"].get("deg", 0))
        
        # Get sunrise/sunset times in local timezone
        timezone_offset = weather_data.get("timezone", 0)
        sunrise = format_time(weather_data["sys"]["sunrise"], timezone_offset)
        sunset = format_time(weather_data["sys"]["sunset"], timezone_offset)

        if output_format == "json":
            # Return machine-readable JSON
            result = {
                "city": weather_data["name"],
                "country": weather_data["sys"]["country"],
                "temperature": temp,
                "feels_like": feels_like,
                "humidity": weather_data["main"]["humidity"],
                "pressure": weather_data["main"]["pressure"],
                "wind": {
                    "speed": wind_speed,
                    "direction": wind_direction
                },
                "weather": weather_data["weather"][0]["description"],
                "air_quality": {
                    "index": aqi_value,
                    "category": aqi_category,
                    "dominant_pollutant": dominant_pollutant,
                    "pollutants": pollutants
                }
            }
            console.print_json(data=result)
        elif output_format == "minimal":
            # Return one-line summary
            console.print(f"{city_name}: {temp}{temp_unit}, {weather_data['weather'][0]['description']}, AQI: {aqi_value or 'N/A'}")
        else:
            # Format last updated time if it's a timestamp
            if isinstance(last_updated, int):
                last_updated = format_time(last_updated, timezone_offset)

            # Prepare forecast section
            forecast_text = ""
            if forecast_data and "list" in forecast_data:
                from datetime import datetime, timezone, timedelta
                forecast_text = "\n[bold]2-Day Forecast[/bold]"
                current_date = None
                tz = timezone(timedelta(seconds=timezone_offset))
                
                for item in forecast_data["list"]:
                    date = datetime.fromtimestamp(item["dt"], tz=timezone.utc).astimezone(tz)
                    if current_date != date.date():
                        current_date = date.date()
                        day_data = [x for x in forecast_data["list"] 
                                if datetime.fromtimestamp(x["dt"], tz=timezone.utc).astimezone(tz).date() == current_date]
                        
                        if len(day_data) > 0:  # Only process if we have data for the day
                            temp_min = min(x["main"]["temp"] for x in day_data)
                            temp_max = max(x["main"]["temp"] for x in day_data)
                            rain_prob = max((x.get("pop", 0) * 100) for x in day_data)
                            
                            if use_fahrenheit:
                                temp_min = (temp_min * 9/5) + 32
                                temp_max = (temp_max * 9/5) + 32
                            
                            emoji = get_weather_emoji(item["weather"][0]["id"])
                            forecast_text += f"\n• {date.strftime('%A')}: {emoji} {temp_min:.1f}{temp_unit} to {temp_max:.1f}{temp_unit} | Rain: {rain_prob:.0f}%"

            # Create the output panel
            output = f"""
{weather_emoji}  {city_name}

[bold]Temperature[/bold]
• Current: {temp:.1f}{temp_unit}
• Feels like: {feels_like:.1f}{temp_unit}
• Humidity: {weather_data['main']['humidity']}%
• Pressure: {weather_data['main']['pressure']} hPa

[bold]Wind[/bold]
• Speed: {wind_speed} m/s
• Direction: {wind_direction} ({weather_data["wind"].get("deg", 0)}°)

[bold]Air Quality[/bold]
• Index: {aqi_value if aqi_value else 'N/A'} ({aqi_category or 'N/A'})
{get_aqi_interpretation(float(aqi_value)) if aqi_value else ''}
• Dominant Pollutant: {dominant_pollutant or 'N/A'}
• Last Updated: {last_updated if last_updated else 'N/A'}
• Source: {aqi_data["source"].title() if aqi_data else 'N/A'}

[bold]Most Significant Pollutants[/bold]
{format_pollutant_display(pollutants)}

[bold]Daily Schedule[/bold]
• Sunrise: {sunrise}
• Sunset: {sunset}
• Weather: {weather_data['weather'][0]['description'].capitalize()}

[bold]2-Day Forecast[/bold]{forecast_text[len("[bold]2-Day Forecast[/bold]"):] if forecast_text else ''}
"""
            console.print(Panel(output.strip(), expand=False))

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@app.command()
def save(
    city: str = typer.Argument(..., help="City name to save"),
    alias: str = typer.Option(None, "--alias", "-a", help="Alias for quick access")
):
    """Save a city with an optional alias for quick access"""
    try:
        # Verify city exists by fetching its weather
        weather_data = get_weather_data(city)
        saved_alias = config.add_city(city, alias)
        console.print(f"[green]✓ Saved {city} with alias '{saved_alias}'[/green]")
    except Exception as e:
        console.print(f"[red]Error: Could not save city - {str(e)}[/red]")

@app.command()
def remove(alias: str = typer.Argument(..., help="Alias of the city to remove")):
    """Remove a saved city"""
    if config.remove_city(alias):
        console.print(f"[green]✓ Removed city with alias '{alias}'[/green]")
    else:
        console.print(f"[red]Error: No city found with alias '{alias}'[/red]")

@app.command()
def list():
    """List all saved cities"""
    cities = config.list_cities()
    if not cities:
        console.print("[yellow]No saved cities found. Use 'meteopoint save CITY' to add one.[/yellow]")
        return

    table = Table(title="Saved Cities")
    table.add_column("Alias", style="cyan")
    table.add_column("City", style="green")
    table.add_column("Default", style="yellow")

    default_city = config.get_default_city()
    for city in cities:
        is_default = "✓" if city["name"] == default_city else ""
        table.add_row(city["alias"], city["name"], is_default)

    console.print(table)

@app.command()
def config_cmd(
    format: str = typer.Option(None, "--format", "-f", help="Output format (pretty/json/minimal)"),
    unit: str = typer.Option(None, "--unit", "-u", help="Temperature unit (celsius/fahrenheit)"),
    default_city: str = typer.Option(None, "--default-city", "-d", help="Set default city")
):
    """Configure MeteoPoint settings"""
    if format:
        if format not in ["pretty", "json", "minimal"]:
            console.print("[red]Error: Format must be pretty, json, or minimal[/red]")
            return
        config.set_format(format)
        console.print(f"[green]✓ Set output format to {format}[/green]")

    if unit:
        if unit not in ["celsius", "fahrenheit"]:
            console.print("[red]Error: Unit must be celsius or fahrenheit[/red]")
            return
        config.set_temperature_unit(unit)
        console.print(f"[green]✓ Set temperature unit to {unit}[/green]")

    if default_city:
        try:
            # Verify city exists
            weather_data = get_weather_data(default_city)
            config.set_default_city(default_city)
            console.print(f"[green]✓ Set default city to {default_city}[/green]")
        except Exception as e:
            console.print(f"[red]Error: Could not set default city - {str(e)}[/red]")

@app.command()
def install_completion():
    """Install shell completion for bash/zsh"""
    import subprocess
    shell = os.environ.get("SHELL", "").split("/")[-1]
    
    if shell == "bash":
        cmd = 'eval "$(register-python-argcomplete meteopoint)"'
        rc_file = os.path.expanduser("~/.bashrc")
    elif shell == "zsh":
        cmd = 'eval "$(register-python-argcomplete meteopoint)"'
        rc_file = os.path.expanduser("~/.zshrc")
    else:
        console.print(f"[red]Unsupported shell: {shell}[/red]")
        return

    with open(rc_file, "a") as f:
        f.write(f"\n# MeteoPoint completion\n{cmd}\n")
    
    console.print(f"[green]✓ Shell completion installed for {shell}[/green]")
    console.print("Please restart your shell or run:")
    console.print(f"source {rc_file}")

if __name__ == "__main__":
    app() 