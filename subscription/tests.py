from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from .models import Subscription


class TestSubscriptionNoAuth(TestCase):
    def test_get_list(self):
        res = self.client.get('/api/subscription')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestSubscription(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'maciej',
            'password123'
        )
        self.client.force_authenticate(self.user)

    def add_subscription(self, currency_name: str):
        payload = {'currency_name': currency_name}
        return self.client.post('/api/subscription', payload)

    def delete_subscription(self, currency_name: str):
        return self.client.delete(f'/api/subscription/{currency_name}')

    def test_get_no_subscriptions(self):
        res = self.client.get('/api/subscription')
        self.assertEqual(res.data, [])

    def test_get_no_subscriptions_with_date(self):
        pass

    def test_add_subscription_no_payload(self):
        res = self.client.post('/api/subscription')
        self.assertEqual(res.status_code, 400)

    def test_add_subscription_with_currency_not_in_system(self):
        res = self.add_subscription('test')
        self.assertEqual(res.status_code, 403)

    def test_add_subscription(self):
        res = self.add_subscription('PLN')
        self.assertEqual(res.status_code, 201)

    def test_add_subscription_lowercase(self):
        res = self.add_subscription('pln')
        self.assertEqual(res.status_code, 201)

    def test_add_duplicate_subscription(self):
        res1 = self.add_subscription('PLN')
        res2 = self.add_subscription('PLN')

        self.assertEqual(res1.status_code, 201)
        self.assertEqual(res2.status_code, 403)

    def test_add_different_subscription(self):
        res1 = self.add_subscription('PLN')
        res2 = self.add_subscription('USD')

        self.assertEqual(res1.status_code, 201)
        self.assertEqual(res2.status_code, 201)

    def test_get_currencies(self):
        pass

    def test_get_currencies_with_changed_base_currency(self):
        pass

    def test_remove_subscription(self):
        _ = self.add_subscription('PLN')
        res_delete = self.delete_subscription('PLN')

        self.assertEqual(res_delete.status_code, 204)

    def test_remove_subscription_lowercase(self):
        _ = self.add_subscription('PLN')
        res_delete = self.delete_subscription('pln')

        self.assertEqual(res_delete.status_code, 204)

    def test_remove_subscription_again(self):
        _ = self.add_subscription('PLN')
        _ = self.delete_subscription('PLN')
        res_delete = self.delete_subscription('PLN')

        self.assertEqual(res_delete.status_code, 404)

    def test_remove_subscription_not_added(self):
        _ = self.add_subscription('PLN')
        res_delete = self.delete_subscription('USD')

        self.assertEqual(res_delete.status_code, 404)

    def test_get_currencies_after_delete(self):
        pass

    def test_get_currencies_after_delete_with_changed_base_currency(self):
        pass
