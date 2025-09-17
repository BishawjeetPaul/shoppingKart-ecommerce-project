from django.shortcuts import render, get_object_or_404, redirect
from category.models import Category
from store.models import Product



# This function for add products.
def add_product(request):
    categories = Category.objects.filter(isDelete=False)
    context = {'categories': categories}

    if request.method == 'POST':
        product_name        = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_price       = request.POST.get('product_price')
        product_image       = request.FILES.get('product_image')
        stock               = request.POST.get('stock')
        category_id         = request.POST.get('category')

        # Fetch category instance
        category = Category.objects.get(id=category_id)

        # Create product
        product = Product.objects.create(
            product_name=product_name,
            product_description=product_description,
            product_price=product_price,
            product_image=product_image,
            stock=stock,
            category=category   # ✅ use category instance
        )
        product.save()

        # Optional: redirect after success
        # return redirect('manage_products')  

    return render(request, 'store/add-products.html', context)


# This function for manage products.
def manage_product(request):
    products = Product.objects.filter(isDelete=False)
    context = {'products': products}
    return render(request, 'store/manage-products.html', context)


# This function for edit-product
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.filter(isDelete=False)
    context = {
        'product': product,
        'categories': categories
    }

    if request.method == 'POST':
        # product_id          = request.POST.get('product_id')
        product_name        = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_price       = request.POST.get('product_price')
        category_id         = request.POST.get('category')
        stock               = request.POST.get('stock')

        # try:
        product.product_name=product_name
        product.product_description=product_description
        product.product_price=product_price
        product.stock=stock
        category = Category.objects.get(id=category_id)
        product.category_id=category

            # Handle image upload
        if request.FILES.get('product_image'):
            product.product_image = request.FILES['product_image']

            # Update category model
        product.save()

            # messages.success(request, "Successfully Updated product")
        return redirect('manage-product')  # ✅ redirect instead of HttpResponseRedirect

        # except Exception as e:
            # messages.error(request, f"Failed to Update product: {str(e)}")
            # return redirect('edit-product', product_id=product.id)  # ✅ redirect back to edit page

    return render(request, 'store/edit-product.html', context)


# This function for delete-product.
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.isDelete=True
    product.save()
    return redirect('manage-product')
