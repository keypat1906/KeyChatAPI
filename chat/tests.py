from django.test import TestCase

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.

class MessageTestCase(TestCase):

    def setUp(self):

        self.client = APIClient()

    def create_users(self):
        body = {"username":"newuser"}

        response = self.client.post('/api/users', body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = {'username': 'olduser'}

        response = self.client.post('/api/users', body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response)


    def create_message(self):
        user1 = self.create_users()
        
        body = {"sender":"newuser","receiver":"olduser","message":"Hiii"}

        response = self.client.post('/api/messages/', body, format='json')
        print(response)
        return response

    def test_create(self):
        response = self.create_message()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.create_message()
        retrieve_response = self.client.get("/api/recent-messages")
        print(retrieve_response)
        self.assertEqual(response.data, retrieve_response.data)
