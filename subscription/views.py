from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Subscription
from .serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post']
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        queryset = Subscription.objects.filter(user_id=self.request.user.id)
        return queryset
