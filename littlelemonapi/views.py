from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from . import serializers
from . import models

class MenuItemsViewSet(ModelViewSet):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer

class CartViewSet(ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer