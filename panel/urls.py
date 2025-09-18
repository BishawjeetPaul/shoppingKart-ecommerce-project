from django.urls import path
from panel import views


urlpatterns = [
    path('dashboard/', views.admin_panel, name="admin-panel"),
    # ------------------------PRODUCT-URLS----------------------------- #
    path('add/product/', views.add_product, name='add-product'),
    path('manage/product/', views.manage_product, name='manage-product'),
    path('edit/product/<uuid:product_id>/', views.edit_product, name='edit-product'),
    path('delete/product/<uuid:product_id>/', views.delete_product, name='delete-product'),
    # ------------------------CATEGORY-URLS---------------------------- #
    path('add/category/', views.add_category, name='add-category'),
    path('manage/category/', views.manage_category, name='manage-category'),
    path('edit/category/<uuid:category_id>/', views.edit_category, name='edit-category'),
    path('delete/category/<uuid:category_id>/', views.delete_category, name='delete-category'),
]
