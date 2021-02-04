import requests
from datetime import datetime

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response

from rest_framework import generics
from rest_framework import serializers
import django_filters.rest_framework

from .models import Subscription
from .serializers import SubscriptionSerializer
from .exceptions import SubscriptionException
from currency_app.settings import CURRENCIES, BASE_CURRENCY, EXCHANGE_URL


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post', 'delete']
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        queryset = Subscription.objects.filter(user_id=self.request.user.id)
        return queryset

    def destroy(self, request, *args, **kwargs):
        user = request.user

        currency_name: str = kwargs['pk'].upper()
        subscription_params = {
            'user': user,
            'currency_name': currency_name
        }
        subscription = Subscription.objects.filter(
            **subscription_params
        ).first()
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise SubscriptionException


class RateViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        res = requests.get(f'{EXCHANGE_URL}/latest').json()
        print('Sending request')

        queryset = Subscription.objects.filter(
            user=request.user
        )
        serializer = SubscriptionSerializer(
            queryset,
            many=True,
            context={
                'user_id': 'request.user.id',
                'res': res
            }
        )

        datetime_now = datetime.now()
        return Response({
            'base_currency': BASE_CURRENCY,
            'date': datetime_now,
            'rates': serializer.data
        })
