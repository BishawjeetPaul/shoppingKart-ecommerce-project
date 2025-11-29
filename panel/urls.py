from django.urls import path
from panel import views


urlpatterns = [
    # --------------------ADMIN-DASHBOARD-URLS------------------------- #
    path('dashboard/', views.admin_panel, name="admin-panel"),
    # ------------------------PRODUCT-URLS----------------------------- #
    path('add/product/', views.add_product, name='add-product'),
    path('manage/product/', views.manage_product, name='manage-product'),
    path('edit/product/<uuid:product_id>/', views.edit_product, name='edit-product'),
    path('delete/product/<uuid:product_id>/', views.delete_product, name='delete-product'),
    path('search/product/', views.search_product, name='search-product'),
    # ------------------------CATEGORY-URLS---------------------------- #
    path('add/category/', views.add_category, name='add-category'),
    path('manage/category/', views.manage_category, name='manage-category'),
    path('edit/category/<uuid:category_id>/', views.edit_category, name='edit-category'),
    path('delete/category/<uuid:category_id>/', views.delete_category, name='delete-category'),
    path('search/category/', views.search_category, name='search-category'),
    # -----------------------VARIATIONS-URLS--------------------------- #
    path('add/variation/', views.add_variation, name='add-variation'),
    path('manage/variation/', views.manage_variation, name='manage-variation'),
    path('edit/variation/<uuid:variation_id>/', views.edit_variation, name='edit-variation'),
    path('delete/variation/<uuid:variation_id>/', views.delete_variation, name='delete-variation'),
    path('search/variation/color/', views.search_color_variation, name='search-color-variation'),
    path('search/variation/size/', views.search_size_variation, name='search-size-variation'),

]
