from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from info.models import Student

class CollegeERPApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.student = Student.objects.create(
            user=self.user,
            USN='123456',
            name='Test Student',
            sex='Male',
        )

    def test_detail_view_unauthenticated(self):
        # Should return 401 Unauthorized due to our DRF IsAuthenticated permission
        response = self.client.get('/api/detail/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_view_authenticated(self):
        # Should return 200 OK
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/detail/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    def test_swagger_ui_loads(self):
        # Ensure our generated Swagger documentation is accessible
        response = self.client.get('/api/docs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
