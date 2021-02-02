from rest_framework import serializers
from currency_app.settings import CURRENCIES, BASE_CURRENCY

from .models import Subscription
from .exceptions import CurrencyException, SubscriptionDuplicateException


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['currency_name', 'id']

    def create(self, validated_data):
        _user_id = self.context['request'].user

        currency_name: str = validated_data['currency_name'].upper()
        if currency_name not in CURRENCIES:
            raise CurrencyException

        subscription_params = {
            'user': _user_id,
            'currency_name': currency_name
        }

        subscription = Subscription.objects.filter(
            **subscription_params
        )
        if subscription:
            raise SubscriptionDuplicateException

        subscription_created = Subscription(
            **subscription_params
        )
        subscription_created.save()
        return subscription_created
