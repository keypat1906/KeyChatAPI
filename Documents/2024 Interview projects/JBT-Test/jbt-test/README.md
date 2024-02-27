
This feature is created to calculate routes for a small pizza chain that recently purchased one drone to deliver their pizzas. Drone range is 25 miles and you can configure that when you create drone object. 

VirtualEnv
First create the virtualenv using below commands.

Install the virtualenv
pip install virtualenv

Initialize the venv in your local dir
virtualenv venv

Activate the virtualenv
source venv/bin/activate

Now you are good to install all of your pip packages.
.//venv/bin/pip install -r requirements.txt

Now the app is ready to test. This app is created in Flask and it has 1 API Endpoint

Run this command to start the app

flask --app src/app run

Now your app is running on port 5000


This code test assumes pizza shop address is = "6138 Bollinger Rd, San Jose, CA 95129" so all the drone delivery will happen from this pizza shop


API Endpoints

1. First endpoint is to calculate the optimal path for given addresses in orders.csv file. I have used Geopy library to calculate the optimal path. 

First I fetched the first address from the CSV file and then using the Geopy library, I fetched the nearest address from rest of the addresses, and after fetching that second address, I repeated the processes and I kept getting nearby addresses.

GET {{server}}//optimal-path

This return the path the drone should take to deliver 

[
    [
        37.30884145,
        -122.00120797064812
    ],
    [
        37.31989615,
        -122.01637004809085
    ],
    [
        37.34102688643793,
        -122.00013308422812
    ],
    [
        37.36113465,
        -121.98953109648113
    ]
]


2.  This endpoint provides the authenticate functionality. Currently only user "admin@jbtc.com" is used for authentication.
This endpoint will return the jwt token which is valid for 1 hour. 
 
POST {{server}}/authenticate

{
    "data": "token",
    "message": "Successfully fetched auth token"
}


3.

POST {{server}}/destination?coordinates=37.461449, -121.912258

This endpoint return "success" : True if drone can deliver to given address, otherwise it will return False if drone is out of range for that address.
{
    "message": "Drone delivered to address 37.461449, -121.912258 with distance 11.710116663456743",
    "success": true
}

If drone is out of range, it will return 500 with message

{
    "message": "Drone battery will out of range to for address 37.366574, -121.963910"
}


Tests

I have added unit tests to test the endpoints 

To run the test, execute below command

pytest

============================================================= test session starts ===============================================================
platform darwin -- Python 3.10.9, pytest-8.0.1, pluggy-1.4.0
rootdir: /JBT-Test/jbt-test
collected 2 items                                                                                                                                

tests/test_endpoint.py ..                                                                                                                  [100%]

=============================================================== 2 passed in 0.67s ===============================================================


Docker

I have included docker-compose file in case you want to create Docker image.
Run this command to create the docker image

docker-compose up


Tests:
I have included 2 test cases one with success 200 and another with failure (no param) 404.



Questions/Concerns:
I used KISS (Keep it Simple,Stupid) principle to create this app. I created utils functinons in separate file. If you have any questions or concerns please reach out to me keyurpatel80@gmail.com

