from rest_framework import serializers

from .models import Subscription
from .exceptions import CurrencyException, SubscriptionDuplicateException
from currency_app.settings import CURRENCIES


class SubscriptionSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ['currency_name', 'rate']

    def get_rate(self, obj):
        currency_name = obj.currency_name
        return self.context.get('res').get('rates').get(currency_name)

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
