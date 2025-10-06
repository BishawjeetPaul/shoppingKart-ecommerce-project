from django.urls import path
from store import views


urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='product_by_category'),
    path('store/category/<slug:category_slug>/<slug:product_slug>/', views.product_details, name='product-details'),
    path('search/', views.search, name='search'),
]
