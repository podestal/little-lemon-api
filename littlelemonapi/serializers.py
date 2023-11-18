from . import models
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ['title']

class MenuItemSerializer(serializers.ModelSerializer):

    category = CategorySerializer

    class Meta:
        model = models.MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']

class CartSerializer(serializers.ModelSerializer):

    total_price = serializers.SerializerMethodField(method_name='calculate_price')


    class Meta:
        model = models.Cart
        fields = ['id', 'quantity', 'unit_price', 'total_price', 'menuitem_id']


    def calculate_price(self, cart: models.Cart):
        return cart.quantity * cart.unit_price


