from django.urls import path
from panel import views


urlpatterns = [
    path('dashboard/', views.admin_panel, name="admin-panel"),
    # -------------------------PRODUCTS-------------------------
    path('products/add-products/', views.add_product, name="add-products"),
    path('products/manage-products/', views.manage_products, name="manage-products"),
]
