from rest_framework import serializers
from rest_framework.exceptions import APIException
from currency_app.settings import CURRENCIES, BASE_CURRENCY

from .models import Subscription


class CurrencyException(APIException):
    status_code = 403
    default_detail = 'This currency doesnt exist in our system.'
    default_code = 'currency_doesnt_exists'


class SubscriptionDuplicateException(APIException):
    status_code = 403
    default_detail = 'User already has a subscription for currency.'
    default_code = 'subscription_duplicate'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['currency_name']

    def create(self, validated_data):
        _user_id = self.context['request'].user

        currency_name: str = validated_data['currency_name'].upper()
        if currency_name not in CURRENCIES:
            raise CurrencyException

        subscription_params = {
            'user': _user_id,
            'currency_name': currency_name
        }

        tmp = Subscription.objects.filter(
            **subscription_params
        )
        if tmp:
            raise SubscriptionDuplicateException

        subscription = Subscription(
            **subscription_params
        )
        subscription.save()
        return subscription
