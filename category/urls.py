from django.urls import path
from category import views


urlpatterns = [
    path('add/category/', views.add_category, name='add-category'),
    path('manage/category/', views.manage_category, name='manage-category'),
    path('edit/category/<uuid:category_id>/', views.edit_category, name='edit-category'),
    path('delete/category/<uuid:category_id>/', views.delete_category, name='delete-category'),
]
