from django.shortcuts import render
from account.models import CustomUser


# this function for admin-customization.
def admin_panel(request):
    return render(request, 'admin-panel.html')


# This function for add products.
def add_product(request):
    return render(request, 'panel/products/add-products.html')


# This function for manage products.
def manage_products(request):
    customers = CustomUser.objects.filter(user_type=2)
    return render(request, 'panel/products/manage-products.html', {'customers': customers})


