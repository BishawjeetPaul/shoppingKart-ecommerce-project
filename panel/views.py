from django.shortcuts import render


# this function for admin-customization.
def admin_panel(request):
    return render(request, 'admin-panel.html')


# This function for add products.
def add_product(request):
    return render(request, 'panel/products/add-products.html')


# This function for manage products.
def manage_products(request):
    return render(request, 'panel/products/manage-products.html')


