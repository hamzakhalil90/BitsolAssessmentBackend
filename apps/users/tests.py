from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from apps.users.models import User, Address, Organization
from apps.users.views import UserAPIView


class UserAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.organization = Organization.objects.create(name="Test Org")
        self.user = User.objects.create(name="Test User", email="test@example.com", organization=self.organization)
        self.address_data = {
            "address_line_1": "123 Test St",
            "city": "Test City",
            "state": "Test State",
            "country": "Test Country",
            "phone_number": "1234567890"
        }

    def test_list_users(self):
        view = UserAPIView.as_view({'get': 'get'})
        request = self.factory.get("/user/")
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        view = UserAPIView.as_view({'post': 'create'})
        data = {
            "name": "New User",
            "email": "newuser@example.com",
            "organization": self.organization.id,
            "address": [self.address_data]
        }
        print(data)
        request = self.factory.post("/user/", data, format='json')
        response = view(request)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_update_user(self):
        view = UserAPIView.as_view({'patch': 'partial_update'})
        updated_data = {
            "id": self.user.guid,
            "name": "Updated User",
            "email": "updateduser@example.com",
            "organization": self.organization.id,
            "address": [self.address_data]
        }
        request = self.factory.patch(f"/user/", updated_data, format='json')
        response = view(request, id=self.user.guid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(guid=self.user.guid).name, "Updated User")

    def test_delete_user(self):
        view = UserAPIView.as_view({'delete': 'destroy'})
        request = self.factory.delete(f"/user/?id={self.user.guid}")
        response = view(request, id=self.user.guid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(guid=self.user.guid).exists())

    def test_invalid_user_creation(self):
        view = UserAPIView.as_view({'post': 'create'})
        # Missing required fields in data
        invalid_data = {"name": "Invalid User"}
        request = self.factory.post("/user/", invalid_data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertFalse(User.objects.filter(name="Invalid User").exists())

    # Add more test cases as needed
