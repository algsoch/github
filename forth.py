from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from google import genai
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the data from a CSV file (assuming the file is named 'output.csv')
# The CSV file should have columns: 'STATION', 'PINCODE'
data = pd.read_csv('output.csv')

# Print the first few rows of the data to verify it is loaded correctly
logger.info(data.head())

# Print the unique station codes to verify they are loaded correctly
logger.info("Unique station codes: %s", data['STATION'].unique())

class StationInfo(BaseModel):
    state_name: str
    district_name: str = None
    pincode: str

def get_location_info(pincode, api_key):
    # This function uses the Google GenAI API to fetch the state_name and district_name
    client = genai.Client(api_key=api_key)
    prompt = f"Get the state and district for the pincode {pincode}"
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    logger.info(f"GenAI API response: {response}")
    if response and response.status == 'success':
        location_data = response.data
        # Assuming the response data is a string and needs to be parsed
        # You might need to adjust this based on the actual response format
        state_name = "Unknown"
        district_name = None
        for line in location_data.split('\n'):
            if "state" in line.lower():
                state_name = line.split(':')[-1].strip()
            if "district" in line.lower():
                district_name = line.split(':')[-1].strip()
        return {
            "state_name": state_name,
            "district_name": district_name
        }
    else:
        return {"state_name": "Unknown", "district_name": None}

@app.get("/station_info/{station_code}", response_model=StationInfo)
async def get_station_info(station_code: str):
    try:
        # Find the row with the given station_code
        row = data[data['STATION'] == int(station_code)]
        
        if row.empty:
            raise HTTPException(status_code=404, detail="Station code not found")
        
        # Extract the pincode
        pincode = row.iloc[0]['PINCODE']
        
        # Get the location info using the Google GenAI API
        api_key = "AIzaSyAK_gs-EXMRAiPkjReZvhqjU2pPD6jpCZ0"  # Replace with your actual API key
        location_info = get_location_info(pincode, api_key)
        
        return StationInfo(state_name=location_info['state_name'], district_name=location_info['district_name'], pincode=pincode)
    except Exception as e:
        logger.error("Error occurred: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# To run the FastAPI app, use the command: uvicorn forth:app --reload