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
        fields = '__all__'

# class CartMenuItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.MenuItem
#         fields = ['id', ]

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cart
        fields = ['id']

    def save(self, **kwargs):
        user_id = self.context['user_id']
        self.instance = models.Cart.objects.create(user_id = user_id, **self.validated_data)
        return self.instance
    

class CartItemSerializer(serializers.ModelSerializer):

    menuitem = MenuItemSerializer()
    class Meta:
        model = models.CartItem
        fields = ['id', 'quantity', 'menuitem']

class CreateCartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.CartItem
        fields = ['menuitem', 'quantity']

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        self.instance = models.CartItem.objects.create(cart_id = cart_id, **self.validated_data)
        return self.instance
    
class AddMenuItemSerializer(serializers.ModelSerializer):

    menuitem_id = serializers.IntegerField()

    class Meta:
        model = models.Cart
        fields = ['menuitem_id', 'quantity', 'price']

    # def save(self, **kwargs):
    #     cart_id = self.context['cart_id']
    #     menu_item_id = self.validated_data['menuitem_id']
    #     quantity = self.validated_data['quantity']


class CartMenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MenuItem
        fields =['title']



    
    


