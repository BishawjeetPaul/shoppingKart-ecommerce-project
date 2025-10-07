from django.urls import path
from carts import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/cart/<uuid:product_id>/', views.add_cart, name='add-cart'),
    path('add/cart/item/<uuid:product_id>/', views.add_cart_item, name='add-cart-item'),
    path('remove/cart/<uuid:product_id>/', views.remove_cart, name='remove-cart'),
    path('remove/cart/item/<uuid:product_id>/', views.remove_cart_item, name='remove-cart-item'),
]
