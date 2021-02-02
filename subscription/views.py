from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response

from .models import Subscription
from .serializers import SubscriptionSerializer
from .exceptions import SubscriptionException


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
