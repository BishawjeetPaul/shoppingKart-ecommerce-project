from django.urls import path
from panel import views


urlpatterns = [
    path('dashboard/', views.admin_panel, name="admin-panel"),
]
