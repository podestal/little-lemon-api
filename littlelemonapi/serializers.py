from . import models
from rest_framework import serializers
from django.contrib.auth.models import Group

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ['title']

class MenuItemSerializer(serializers.ModelSerializer):

    category = CategorySerializer()

    class Meta:
        model = models.MenuItem
        fields = ['id', 'title', 'featured', 'unit_price', 'category']

class SimpleMenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MenuItem
        fields = ['title', 'unit_price']
    

class CartItemSerializer(serializers.ModelSerializer):

    menuitem = SimpleMenuItemSerializer()
    price = serializers.SerializerMethodField(method_name='get_price')
    class Meta:
        model = models.CartItem
        fields = ['id', 'quantity', 'menuitem', 'price']

    def get_price(self ,cart_item: models.CartItem):
        return cart_item.menuitem.unit_price * cart_item.quantity

class CreateCartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.CartItem
        fields = ['menuitem', 'quantity']

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        self.instance = models.CartItem.objects.create(cart_id = cart_id, **self.validated_data)
        return self.instance
    
class CartSerializer(serializers.ModelSerializer):

    cart_items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = models.Cart
        fields = ['id', 'cart_items', 'total_price']

    def save(self, **kwargs):
        user_id = self.context['user_id']
        self.instance = models.Cart.objects.create(user_id = user_id, **self.validated_data)
        return self.instance
    
    def get_total_price(self, cart:models.Cart):
        return sum(cartitem.menuitem.unit_price * cartitem.quantity for cartitem in cart.cart_items.all())
    
class AddMenuItemSerializer(serializers.ModelSerializer):

    menuitem_id = serializers.IntegerField()

    class Meta:
        model = models.Cart
        fields = ['menuitem_id', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = '__all__'


class GroupSerizlizer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'
