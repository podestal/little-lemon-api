from django.shortcuts import render
from django.conf import settings
from djoser.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth.models import Group
from rest_framework.decorators import permission_classes, action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from . import serializers
from . import models
from . import permissions
from core.models import User

class MenuItemsViewSet(ModelViewSet):
    queryset = models.MenuItem.objects.select_related('category').all()
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class CartViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        return models.Cart.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateCartSerializer
        return serializers.CartSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

class CartItemViewSet(ModelViewSet):
    queryset = models.CartItem.objects.all()
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return models.CartItem.objects.filter(cart_id = self.kwargs['cart_pk'])

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateCartItemSerializer
        return serializers.CartItemSerializer
    
class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        if self.request.user.is_staff:
            if self.request.query_params.get('status') == 'pending':
                return models.Order.objects.filter(status=False)
            elif self.request.query_params.get('status') == 'delivered':
                return models.Order.objects.filter(status=True)
            return models.Order.objects.all()
        return models.Order.objects.filter(user_id = self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateOrderSerializer
        if self.request.method == 'PATCH' or self.request.method == 'PUT' and self.request.user.is_staff and not self.request.user.is_superuser:
            return serializers.PatchOrderSerializer
        return serializers.OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

class OrderItemViewSet(ModelViewSet):

    serializer_class = serializers.OrderItemSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return models.OrderItem.objects.filter(order_id=self.kwargs['orders_pk'])

class UserViewSet(ModelViewSet):

    permission_classes = [permissions.IsAdminOrReadOnlyOrIsAnonymous]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        # groups = []
        # for group in self.request.user.groups.all():
        #     groups.append(group.name)
        # print(groups)
        # print(len(self.request.META['PATH_INFO'].split('/')))
        # group = Group.objects.get(name=self.request.META['PATH_INFO'].split('/')[-3])
        # print(group)
        if self.request.user.is_superuser:
            # print(self.request.META['PATH_INFO'].split('/')[3])
            # if len(self.request.META['PATH_INFO'].split('/')) > 5:
            #     group_name = self.request.META['PATH_INFO'].split('/')[3]
            #     group = Group.objects.get(name=group_name)
            #     return User.objects.filter(groups=group.id)
            return User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

    
    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        user = User.objects.get(id = self.request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        print('kwargs', self.kwargs)
        user = request.data['username']
        print(user)
        group = Group.objects.get(id = self.kwargs['groups_pk'])
        if request.method == 'PUT':
            group.user_set.add(user)
        return Response('Group Updated')

class GroupViewSet(ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    @action(detail=False, methods=['GET', 'PUT', 'PATCH'])
    def manager(self, request):
        return Response('Managers')
    
    @action(detail=False, methods=['GET', 'PUT', 'PATCH'])
    def delivery_crew(self, request):
        if request.method == 'PUT':
            return Response('posted')
        return Response('Devilvery Crew')
    
    @api_view(['GET', 'PATCH', 'DELETE'])
    def manager(request):
        group = Group.objects.get(name='manager')
        print(request.user.is_superuser)
        if request.method == 'GET':
            print(request.data)
            users = User.objects.filter(groups=group.id)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            user = User.objects.get(username = request.data['username'])
            group.user_set.add(user)
            return Response(f'User added to {group} group')
        elif request.method == 'DELETE':
            user = User.objects.get(username = request.data['username'])
            group.user_set.remove(user)
            return Response(f'User removed from {group} group')
            
            


    @api_view(['GET', 'PATCH', 'DELETE'])
    def delivery_crew(request):
        group = Group.objects.get(name='delivery crew')
        print(request.user.is_superuser)
        if request.method == 'GET':
            print(request.data)
            users = User.objects.filter(groups=group.id)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            user = User.objects.get(username = request.data['username'])
            group.user_set.add(user)
            return Response(f'User add to {group} group')
        elif request.method == 'DELETE':
            user = User.objects.get(username = request.data['username'])
            group.user_set.remove(user)
            return Response(f'User removed from {group} group')
    
    

    
    