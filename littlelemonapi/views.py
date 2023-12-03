from django.shortcuts import render
from django.conf import settings
from djoser.serializers import UserSerializer
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from . import serializers
from . import models
from . import permissions
from core.models import User

class MenuItemsViewSet(ModelViewSet):
    queryset = models.MenuItem.objects.select_related('category').all()
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]

    # def get_serializer_class(self):
    #     if self.request.path == 'POST':
    #         return serializers.AddMenuItemSerializer
    #     return serializers.MenuItemSerializer
    


class CartViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        return models.Cart.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateCartSerializer
        return serializers.CartSerializer

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

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateOrderSerializer
        return serializers.OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

class OrderItemViewSet(ModelViewSet):
    queryset = models.OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer
    permission_classes = [IsAuthenticated]

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class GroupViewSet(ModelViewSet):

    queryset = Group.objects.all()

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs['users_pk']
        group_name = request.data['name']
        user = User.objects.get(id=user_id)
        group = Group.objects.get(name=group_name)
        group.user_set.add(user)
        return Response(f'{user} added to group {group_name}')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AssignUserToGroupSerializer
        return serializers.GroupSerializer
    

    
    