from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . import serializers
from . import models
from . import permissions

class MenuItemsViewSet(ModelViewSet):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]


class CartViewSet(ModelViewSet):
    queryset = models.Cart.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddMenuItemSerializer
        return serializers.CartSerializer

    def get_serializer_context(self):

        return {'user_id': self.request.user.id, 'cart_id': self.kwargs.get('pk') }

