from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from . import serializers
from . import models
from . import permissions

class MenuItemsViewSet(ModelViewSet):
    queryset = models.MenuItem.objects.all()
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get_serializer_class(self):
        print(self.kwargs)
        if self.request.path == '/api/cart/1/menu-items/':
            return serializers.CartMenuItemSerializer
        return serializers.MenuItemSerializer
    


class CartViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Cart.objects.filter(user = self.request.user.id).select_related('menuitem')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateCartSerializer
        return serializers.CartSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'cart_id': self.kwargs.get('pk') }

