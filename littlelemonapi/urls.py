from rest_framework_nested import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register('menu-items', views.MenuItemsViewSet)
router.register('cart', views.CartViewSet)

carts_router = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
carts_router.register('menu-items', views.MenuItemsViewSet, basename='cart-items')

# urlpatterns = [
    # path('menu-items/', views.MenuItemsViewSet.as_view())
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>', views.CollectionDetail.as_view())
# ]

urlpatterns = router.urls + carts_router.urls