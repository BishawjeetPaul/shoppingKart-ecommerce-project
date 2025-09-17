from django.urls import path
from category import views


urlpatterns = [
    path('add-category/', views.add_category, name='add-category'),
    path('manage-category/', views.manage_category, name='manage-category'),
]
