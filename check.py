from flask import Flask, jsonify
import pandas as pd
from google import genai

# Gemini AI setup
client = genai.Client(api_key="AIzaSyAK_gs-EXMRAiPkjReZvhqjU2pPD6jpCZ0")

# Flask app initialization
app = Flask(__name__)

# Load CSV file
csv_file = "output.csv"  # Ensure this file is in the same directory
df = pd.read_csv(csv_file)

def get_location_info(pincode, api_key):
    # This function uses the Google GenAI API to fetch the state_name and district_name
    client = genai.Client(api_key=api_key)
    prompt = f"Get the state and district for the pincode {pincode}"
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    if response and response.status == 'success':
        location_data = response.data
        return {
            "state_name": location_data.get("state_name", "Unknown"),
            "district_name": location_data.get("district_name", None)
        }
    else:
        return {"state_name": "Unknown", "district_name": None}

@app.route('/station/<code>', methods=['GET'])
def get_station_info(code):
    # Check if STATION code exists
    station_data = df[df['STATION'] == int(code)]
    
    if not station_data.empty:
        # Extract Pincode
        pincode = str(station_data['PINCODE'].values[0])  # Ensure string format
        
        # Get the location info using the Google GenAI API
        api_key = "AIzaSyAK_gs-EXMRAiPkjReZvhqjU2pPD6jpCZ0"  # Replace with your actual API key
        location_info = get_location_info(pincode, api_key)
        
        return jsonify({"state_name": location_info['state_name'], "district_name": location_info['district_name'], "pincode": pincode})
    else:
        return jsonify({"error": "Station code not found"}), 404

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
