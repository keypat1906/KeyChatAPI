from flask import Flask, jsonify, Response, request
import csv
import jwt
import datetime 
import geopy.distance
from geopy import Nominatim
from geopy.distance import great_circle
from .drone import drone
from .utils import (validate_token, 
                   can_deliver_diff_address, 
                   can_deliver_same_address
)


geolocator = Nominatim(user_agent="drone_delivery")

pizza_shop_address = "6138 Bollinger Rd, San Jose, CA 95129"
pizza_location = geolocator.geocode(pizza_shop_address)
pizza_location_coordinates = (pizza_location.latitude, pizza_location.longitude)

drone.set_address(pizza_location_coordinates)

filename = "src/orders.csv"

app = Flask(__name__) 


@app.route("/optimal-path")
def optimal_path() -> Response:
    '''
    Function to get optimal path 
    Return the addresses in shortest distance
    '''    

    # Check if jwt token sent is valid
    header = request.headers.get("Authorization")
    if not header:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    token = header.split()[1]
    
    decoded, msg = validate_token(token)
    if not decoded:
        return msg         
   
    # Check if jwt token sent is valid
    locations = []
    sorted_locations = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[1] == 'address':
                continue
            coordintes = geolocator.geocode(row[1])
            locations.append((coordintes.latitude, coordintes.longitude))
    i = 0
    sorted_locations.append(locations[0])
    s_location=sorted_locations[0]
    locations.remove(s_location)

    while i < len(locations):
        nearest_location = min(locations, key=lambda x: great_circle(s_location, x).miles)
        sorted_locations.append(nearest_location)
        s_location = nearest_location
        locations.remove(s_location)
        i += 1
    sorted_locations.extend(locations)
    return jsonify(sorted_locations)


@app.route("/destination")
def destination() -> Response:
    '''
    Function to go to next destination
    Success - If drone can deliver pizza in given range
    Fail - If drone cannot deliver pizza in given range
    '''    
    # Check if jwt token sent is valid
    header = request.headers.get("Authorization")
    if not header:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    token = header.split()[1]
    
    decoded, msg = validate_token(token)
    if not decoded:
        return msg         
   
    # get destionation coordinates
    address = request.args.get('coordinates')
    if not address:
         return jsonify({"message": "address not entered"}),404
    
    print("current drone range", drone.get_remaining_range())
    
    #coordinates = geolocator.geocode(address)
    coordinates_1 = address.split(',')[0]
    coordinates_2 = address.split(',')[1]
    
    pizza_distance_to_new_address = geopy.distance.geodesic((pizza_location.latitude,
                                 pizza_location.longitude),
                                 (coordinates_1, coordinates_2)).miles
    # Check if drone starting address is same as pizza shop address
    if drone.address == pizza_location_coordinates:
        return can_deliver_same_address(pizza_distance_to_new_address, 
                                        coordinates_1, 
                                        coordinates_2, 
                                        address)
    else:
        return can_deliver_diff_address(pizza_distance_to_new_address, 
                                        coordinates_1, 
                                        coordinates_2, 
                                        address)
        
    return jsonify({"success": True, "distance": pizza_distance_to_new_address})


@app.route("/authenticate", methods=["POST"])
def authenticate():
    '''
    This is authenticate endpoint
    return the jwt token if successful
    return error if fail to create jwt
    '''
    data = request.json
    email = data["email"]
    if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
        }, 400
        # validate input
    try:
        expire = datetime.datetime.utcnow() + datetime.timedelta(
                    minutes=60
                )
        jwt_data = {"exp": expire, "shop_address": pizza_shop_address}
        token = jwt.encode(
                jwt_data,
                email,
                algorithm="HS256"
        )
        return {
                    "message": "Successfully fetched auth token",
                    "data": token
            }
    except Exception as e:
            return {
                    "error": "Something went wrong",
                    "message": str(e)
            }, 500
  
    