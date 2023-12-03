from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from . import serializers
from . import models
from . import permissions

class MenuItemsViewSet(ModelViewSet):
    queryset = models.MenuItem.objects.select_related('category').all()
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]

    # def get_serializer_class(self):
    #     if self.request.path == 'POST':
    #         return serializers.AddMenuItemSerializer
    #     return serializers.MenuItemSerializer
    


class CartViewSet(ModelViewSet):

    queryset = models.Cart.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    # def get_queryset(self):
    #     return models.Cart.objects.filter(user = self.request.user.id).select_related('menuitem')

    # def get_serializer_class(self):
    #     if self.request.method == 'POST':
    #         return serializers.CreateCartSerializer
    #     return serializers.CartSerializer

    # def get_serializer_context(self):
    #     return {'user_id': self.request.user.id, 'cart_id': self.kwargs.get('pk') }

class CartItemViewSet(ModelViewSet):
    queryset = models.CartItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateCartItemSerializer
        return serializers.CartItemSerializer
    
class OrderViewSet(ModelViewSet):
    queryset = models.Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.OrderSerializer

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        admin = Group.objects.get(name='Admin')
        # print(admin.user_get())
        return serializers.GroupSerizlizer
