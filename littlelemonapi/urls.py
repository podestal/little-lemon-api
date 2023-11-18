from rest_framework import routers
from django.urls import path
from . import views

router = routers.SimpleRouter()
router.register('menu-items', views.MenuItemsViewSet)
router.register('cart', views.CartViewSet)

# urlpatterns = [
    # path('menu-items/', views.MenuItemsViewSet.as_view())
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>', views.CollectionDetail.as_view())
# ]

urlpatterns = router.urls