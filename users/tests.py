from django.test import TestCase
from rest_framework import status


user = {
    'email': 'maciej@gmail.com',
    'password': 'password123'
}


class TestUserRegister(TestCase):
    def register(self, payload):
        return self.client.post('/api/register', payload)

    def test_register_email(self):
        res = self.register(user)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_register_username(self):
        res = self.register({
            'username': 'maciej',
            'password': 'password123'
        })
        self.assertEqual(res.status_code, 400)

    def test_register_duplicate_email(self):
        _ = self.register(user)
        res = self.register(user)
        self.assertEqual(res.status_code, 400)

    def test_get_token(self):
        _ = self.register(user)
        res = self.client.post('/api/token/', {
            'username': 'maciej@gmail.com',
            'password': 'password123'
        })
        token = res.data.get('access')
        refresh_token = res.data.get('refresh')

        self.assertEqual(res.status_code, 200)
        self.assertTrue(isinstance(token, str))
        self.assertTrue(isinstance(refresh_token, str))

    def test_refresh_token(self):
        _ = self.register(user)
        res = self.client.post('/api/token/', {
            'username': 'maciej@gmail.com',
            'password': 'password123'
        })
        token_refresh = res.data.get('refresh')
        res_refresh = self.client.post('/api/token/refresh/', {
            'refresh': token_refresh
        })
        new_access = res_refresh.data.get('access')

        self.assertEqual(res_refresh.status_code, 200)
        self.assertTrue(isinstance(new_access, str))
