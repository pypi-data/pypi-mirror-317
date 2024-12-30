import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from meteopoint.city_aliases import COMMON_ALIASES

CONFIG_DIR = os.path.expanduser("~/.config/meteopoint")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
CITIES_FILE = os.path.join(CONFIG_DIR, "cities.json")

class Config:
    def __init__(self):
        self.config: Dict = {
            "temperature_unit": "celsius",
            "default_city": None,
            "format": "pretty",
            "api_keys": {
                "openweather": os.getenv("OPENWEATHER_API_KEY"),
                "google_maps": os.getenv("GOOGLE_MAPS_API_KEY")
            }
        }
        self.cities: Dict[str, str] = {}  # user aliases -> city name
        self._load()

    def _ensure_config_dir(self):
        """Ensure configuration directory exists"""
        os.makedirs(CONFIG_DIR, exist_ok=True)

    def _load(self):
        """Load configuration and cities from files"""
        self._ensure_config_dir()
        
        # Load main config
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    self.config.update(json.load(f))
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {CONFIG_FILE}")
        
        # Load saved cities
        if os.path.exists(CITIES_FILE):
            try:
                with open(CITIES_FILE, 'r') as f:
                    self.cities = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {CITIES_FILE}")

    def save(self):
        """Save current configuration to files"""
        self._ensure_config_dir()
        
        # Save main config
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
        
        # Save cities
        with open(CITIES_FILE, 'w') as f:
            json.dump(self.cities, f, indent=2)

    def add_city(self, city: str, alias: Optional[str] = None) -> str:
        """Add a city with optional alias"""
        if alias is None:
            alias = city.lower().replace(" ", "_")
        self.cities[alias] = city
        self.save()
        return alias

    def remove_city(self, alias: str) -> bool:
        """Remove a city by its alias"""
        if alias in self.cities:
            del self.cities[alias]
            self.save()
            return True
        return False

    def get_city(self, alias: str) -> Optional[str]:
        """Get city name by alias, checking both user aliases and built-in aliases"""
        # Check user aliases first (they take precedence)
        if alias in self.cities:
            return self.cities[alias]
        # Then check built-in aliases
        return COMMON_ALIASES.get(alias.lower())

    def get_all_aliases(self) -> List[str]:
        """Get all available aliases (both user-defined and built-in)"""
        # Combine built-in and user aliases, user aliases take precedence
        all_aliases = {**COMMON_ALIASES, **self.cities}
        return sorted(all_aliases.keys())

    def list_cities(self) -> List[Dict[str, str]]:
        """List all saved cities and built-in aliases"""
        user_cities = [{"alias": k, "name": v, "type": "user"} for k, v in self.cities.items()]
        builtin_cities = [{"alias": k, "name": v, "type": "built-in"} 
                         for k, v in COMMON_ALIASES.items() 
                         if k not in self.cities]  # Only show if not overridden
        return user_cities + builtin_cities

    def set_default_city(self, city: str):
        """Set default city"""
        self.config["default_city"] = city
        self.save()

    def get_default_city(self) -> Optional[str]:
        """Get default city"""
        return self.config.get("default_city")

    def set_temperature_unit(self, unit: str):
        """Set temperature unit (celsius/fahrenheit)"""
        if unit.lower() in ["celsius", "fahrenheit"]:
            self.config["temperature_unit"] = unit.lower()
            self.save()

    def get_temperature_unit(self) -> str:
        """Get temperature unit"""
        return self.config.get("temperature_unit", "celsius")

    def set_format(self, format: str):
        """Set output format (pretty/json/minimal)"""
        if format.lower() in ["pretty", "json", "minimal"]:
            self.config["format"] = format.lower()
            self.save()

    def get_format(self) -> str:
        """Get output format"""
        return self.config.get("format", "pretty") 