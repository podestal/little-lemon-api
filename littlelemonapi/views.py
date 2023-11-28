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
    serializer_class = serializers.CartSerializer

