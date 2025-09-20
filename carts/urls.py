from django.urls import path
from carts import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/cart/<uuid:product_id>/', views.add_cart, name='add-cart'),
]
