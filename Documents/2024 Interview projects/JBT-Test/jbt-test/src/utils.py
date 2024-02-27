
from flask import jsonify 
import jwt
from .drone import drone
import geopy.distance



def can_deliver_diff_address(pizza_distance_to_new_address, 
                             coordinates_1, 
                             coordinates_2, 
                             address):
    '''
    Function which check if pizza can be delivered
    return 200 if delivery is successful
    return 400 if pizza cannot be deliver
    '''
    # calcuate the distance from current coordinates to new address
    if drone.address == (coordinates_1, coordinates_2):
         return jsonify({"message": 
                        f"Specified address is same as current drone address"}), 400
    new_distance = geopy.distance.geodesic(drone.address,
                                 (coordinates_1, coordinates_2)).miles
    if new_distance + pizza_distance_to_new_address < drone.get_remaining_range():
        drone.set_address((coordinates_1, coordinates_2))
        drone.set_distance(pizza_distance_to_new_address) 
        return jsonify({"success": True, "message": 
                        f"Drone delivered to address {address} with distance {pizza_distance_to_new_address}"})

    else:
        return jsonify({"message": f"Drone battery will out of range to for address {address}"}),400
             


def can_deliver_same_address(pizza_distance_to_new_address, 
                             coordinates_1, 
                             coordinates_2, 
                             address):
    '''
    Function which if destination is same address again
    return 200 if delivery is successful
    return 400 if pizza cannot be deliver
    '''
    if pizza_distance_to_new_address * 2 < drone.get_remaining_range():
        drone.set_address((coordinates_1, coordinates_2))
        drone.set_distance(pizza_distance_to_new_address) 

        return jsonify({"success": True, "message": 
            f"Drone delivered to address {address} with distance {pizza_distance_to_new_address}"})
               
    else:
        return jsonify({"message": f"Drone battery will out of range to for address {address}"}),400


def validate_token(token):
    '''
    function validate the token signature, iss and expiration
    '''
    try:
        decoded = jwt.decode(token, "admin@jbtc.com", algorithms="HS256")
    
    except jwt.ExpiredSignatureError as e :
        return (None, jsonify({"success": False,"info":f"Expired Signature - {e} Authenticate again"}))
    
    except jwt.DecodeError as e: 
        return (None, jsonify({"success": False,"info":f"Decode Error - {e}"}))
    
    except jwt.InvalidTokenError as e :
        return (None, jsonify({"success": False,"info":f"Invlid Token - {e}"}))
    
    if decoded["shop_address"] != "6138 Bollinger Rd, San Jose, CA 95129":
        return (None, jsonify({"success": False, "info":"Invlid Issuer"}))
   
    return decoded, ""