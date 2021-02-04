from datetime import datetime

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .models import Subscription
from .serializers import SubscriptionSerializer, CurrencySerializer
from .exceptions import SubscriptionException, DateException
from currency_app.settings import BASE_CURRENCY
from subscription.api import get_exchange


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

    def list(self, request, *args, **kwargs):
        base_currency: str = request.query_params.get('base_currency')
        if base_currency is None:
            base_currency = BASE_CURRENCY

        base_currency = base_currency.upper()

        param_date: str = request.query_params.get('date')
        exchange_date = param_date
        if exchange_date:
            try:
                date_object = datetime.strptime(exchange_date, '%Y-%m-%d')
                is_today = date_object.date() == datetime.today().date()
                if is_today:
                    exchange_date = None
            except ValueError:
                raise DateException
        else:
            param_date = datetime.now().date().strftime('%Y-%m-%d')

        res = get_exchange(base_currency, exchange_date)
        print('Sending request')

        queryset = Subscription.objects.filter(
            user=request.user
        )
        serializer = CurrencySerializer(
            queryset,
            many=True,
            context={
                'user_id': 'request.user.id',
                'res': res
            }
        )

        return Response({
            'base_currency': base_currency,
            'date': param_date,
            'rates': serializer.data
        })
