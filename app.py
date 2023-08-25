from flask import Flask, render_template, request, jsonify
import os
import googlemaps
import json
from flask import session

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

app.secret_key = os.getenv("SECRET")



# Initialize Google Maps client
gmaps = googlemaps.Client(key=os.getenv("YOUR_API_KEY"))

@app.route('/')
def index():
    return render_template('input.html', api_key=os.getenv("YOUR_API_KEY"))


@app.route('/map', methods=['GET', 'POST'])
def map():
    if request.method == 'POST':
        session['location'] = request.form.get('location')
    return render_template('map.html', api_key=os.getenv("YOUR_API_KEY"))

@app.route('/get_places', methods=['POST'])
def get_places():
    location = request.json.get('location')
    
    latlng, nearby_places = get_apartment_and_nearby_places(location)
    
    return jsonify({
        "latlng": latlng,
        "places": nearby_places
    })

def get_nearby_places(lat, lng, place_types=["hospital", "school", "bus_stop", "subway_station"]):
    places_data = {}

    for place_type in place_types:
        result = gmaps.places_nearby(location=(lat, lng), radius=1500, type=place_type)
        places_data[place_type] = result.get("results", [])
    
    return places_data

def get_apartment_and_nearby_places(location, place_types=["hospital", "school", "bus_stop", "subway_station"]):
    geocode_result = gmaps.geocode(location)
    latlng = geocode_result[0]["geometry"]["location"]

    nearby_places = get_nearby_places(latlng["lat"], latlng["lng"], place_types)
    
    return latlng, nearby_places

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

