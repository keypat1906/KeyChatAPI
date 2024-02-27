from src.app import app # Flask instance of the API

def test_destination_with_data():
    endpoint = '/destination?coordinates=' + str("29.74,-95.5")
    response = app.test_client().get(endpoint)
    assert response.status_code == 200



def test_destination_with_no_data():
    endpoint = '/destination'
    response = app.test_client().get(endpoint)
    assert response.status_code == 200

