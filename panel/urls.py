from django.urls import path
from panel import views


urlpatterns = [
    path('dashboard/', views.admin_panel, name="admin-panel"),
    # -------------------------PRODUCTS-------------------------
    path('products/add-product/', views.add_product, name="add-product"),
    path('products/manage-product/', views.manage_product, name="manage-product"),
]
