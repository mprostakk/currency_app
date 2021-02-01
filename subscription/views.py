from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny


from .models import Subscription
from .serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get']

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
