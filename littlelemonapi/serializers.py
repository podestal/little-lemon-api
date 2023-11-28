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

    # total_price = serializers.SerializerMethodField(method_name='calculate_price')
    user_id = serializers.IntegerField()
    menuitem_id = serializers.IntegerField()

    class Meta:
        model = models.Cart
        fields = ['user_id', 'id', 'quantity', 'menuitem_id', 'unit_price', 'price']


    def calculate_price(self, cart: models.Cart):
        return cart.quantity * cart.unit_price
    
class AddMenuItemSerializer(serializers.ModelSerializer):

    menuitem_id = serializers.IntegerField()

    class Meta:
        model = models.Cart
        fields = ['menuitem_id', 'quantity']

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        menu_item_id = self.validated_data['menuitem_id']
        quantity = self.validated_data['quantity']
        


    
    


