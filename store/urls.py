from django.urls import path
from store import views


urlpatterns = [
    path('add/product/', views.add_product, name='add-product'),
    path('manage/product/', views.manage_product, name='manage-product'),
    path('edit/product/<uuid:product_id>/', views.edit_product, name='edit-product'),
    path('delete/product/<uuid:product_id>/', views.delete_product, name='delete-product'),
]
