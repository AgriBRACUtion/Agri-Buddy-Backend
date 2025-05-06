from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langgraph.prebuilt import create_react_agent
from langchain.tools import Tool
from dotenv import load_dotenv
import random
import requests
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# Get API key from environment variables
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
if not WEATHER_API_KEY:
    logger.warning("WEATHER_API_KEY not found in environment variables, using hardcoded key")

os.environ["OPENWEATHERMAP_API_KEY"] = WEATHER_API_KEY

def get_current_weather(location):
    """Get weather information in a given location with improved error handling"""
    try:
        logger.info(f"Fetching weather for location: {location}")
        
        # Initialize the OpenWeatherMap wrapper
        weather = OpenWeatherMapAPIWrapper()
        
        # Call the API and get weather data
        weather_data = weather.run(location)
        
        logger.info(f"Successfully retrieved weather data for {location}")
        return weather_data
    
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        
        # Provide fallback response instead of failing completely
        return (f"Unable to fetch weather data for {location}. "
                f"Error: {str(e)}. Please check if the location is valid or try again later.")

# Initialize the tool
weather_info_tool = Tool(
    name="weather_info_tool",
    func=get_current_weather,
    description="Fetches weather information for a given location"
)