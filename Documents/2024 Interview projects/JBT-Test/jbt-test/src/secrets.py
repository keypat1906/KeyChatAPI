import geopy.distance

from geopy import Nominatim
from .drone import Drone

drone = Drone()

geolocator = Nominatim(user_agent="drone_delivery")

pizza_shop_address = "6138 Bollinger Rd, San Jose, CA 95129"


pizza_location = geolocator.geocode(pizza_shop_address)
pizza_location_coordinates = (pizza_location.latitude, pizza_location.longitude)
drone.set_address(pizza_location_coordinates)