from rest_framework_nested import routers
from django.conf import settings
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register('menuitems', views.MenuItemsViewSet)
router.register('cart', views.CartViewSet, basename='cart')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('users', views.UserViewSet, basename='users')
router.register('groups', views.GroupViewSet)

carts_router = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
carts_router.register('cartitems', views.CartItemViewSet, basename='cart-items')

orders_router = routers.NestedDefaultRouter(router, 'orders', lookup='orders')
orders_router.register('orderitems', views.OrderItemViewSet, basename='order-items')


urlpatterns = [
    path('groups/manager/users/', views.GroupViewSet.manager),
    path('groups/delivery-crew/users/', views.GroupViewSet.delivery_crew),
    # path('menu-items/', views.MenuItemsViewSet.as_view())
    # path('products/', views.ProductList.as_view()),
    # path('products/<int:pk>', views.ProductDetail.as_view()),
    # path('collections/', views.CollectionList.as_view()),
    # path('collections/<int:pk>', views.CollectionDetail.as_view())
]

urlpatterns += router.urls + carts_router.urls + orders_router.urls