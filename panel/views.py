from django.shortcuts import render, get_object_or_404, redirect
from category.models import Category
from store.models import Product, Variation
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# this function for admin-customization.
def admin_panel(request):
    return render(request, 'admin-panel.html')

# --------------------CATEGORY-FUNCTIONS------------------ #
# This function for add category
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description')
        category_image = request.FILES.get('category_image')

        categories = Category.objects.create(
            category_name=category_name,
            category_description=category_description,
            category_image=category_image
        )
        categories.save()

    return render(request, 'panel/category/add-category.html')


# This function for manage category
def manage_category(request):
    categories = Category.objects.filter(isDelete=False).order_by('id')
    paginator = Paginator(categories, 10)
    page = request.GET.get('page')
    categories = paginator.get_page(page)
    context = {
		'categories': categories,
	}
    print(categories)
    return render(request, 'panel/category/manage-category.html', context)


# This function for search category
def search_category(request):
    categories = Category.objects.none() # safe empty queryset
    category_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            categories = Category.objects.order_by('created_at').filter(
                Q(category_name__icontains=keyword) |
                Q(category_description__icontains=keyword) |
                Q(slug__icontains=keyword)
            )
            category_count = categories.count()
    context = {
        'categories': categories,
        'category_count': category_count
    }
    return render(request, 'panel/category/manage-category.html', context)


# This function is use for edit category
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    context = {'category': category}

    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description')

        try:
            category.category_name = category_name
            category.category_description = category_description
            # Handle image upload
            if request.FILES.get('category_image'):
                category.category_image = request.FILES['category_image']

            # Update category model
            category.save()

            # messages.success(request, "Successfully Updated Category")
            return redirect('manage-category')  # ✅ redirect instead of HttpResponseRedirect

        except Exception as e:
            # messages.error(request, f"Failed to Update Category: {str(e)}")
            return redirect('edit-category', category_id=category.id)  # ✅ redirect back to edit page

    return render(request, 'panel/category/edit-category.html', context)


# This function is use for delete category
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.isDelete=True
    category.save()
    return redirect('manage-category')

# --------------------PRODUCT-FUNCTIONS------------------- #

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

    return render(request, 'panel/product/add-products.html', context)


# This function for manage products.
def manage_product(request):
    products = Product.objects.filter(isDelete=False).order_by('id')
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {
        'products': products
    }
    print(products)
    return render(request, 'panel/product/manage-products.html', context)


# This function for search category.
def search_product(request):
    products = Product.objects.none()
    products_count = 0

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        
        if keyword:
            products = Product.objects.order_by('created_at').filter(
                Q(product_name__icontains=keyword) |
                Q(product_description__icontains=keyword) |
                Q(slug__icontains=keyword) |
                Q(product_price__icontains=keyword) |
                Q(is_available__icontains=keyword)
            )
            products_count = products.count()
        context = {
            'products': products,
            'products_count': products_count
        }
    return render(request, 'panel/product/manage-products.html', context)


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

        try:
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

        except Exception as e:
            # messages.error(request, f"Failed to Update product: {str(e)}")
            return redirect('edit-product', product_id=product.id)  # ✅ redirect back to edit page
    return render(request, 'panel/product/edit-product.html', context)


# This function for delete-product.
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.isDelete=True
    product.save()
    return redirect('manage-product')


# -----------------------VARIATION------------------------ #

# Variation category choices
variation_category_choice = (
    ('color', 'color'),
    ('size', 'size')
)

def add_variation(request):
    products = Product.objects.filter(isDelete=False)
    variations = Variation.objects.all().order_by('-created_at')

    if request.method == 'POST':
        product_id      = request.POST.get('product')
        category        = request.POST.get('variation_category')
        value           = request.POST.get('variation_value')
        is_active       = request.POST.get('is_active') == 'on'

        product = get_object_or_404(Product, id=product_id)

        # create the variation instance
        variation = Variation.objects.create(
            product             = product,
            variation_category  = category,
            variation_value     = value,
            is_active           = is_active
        )
        variation.save()

    context = {
        'products': products,
        'variations': variations,
        'variation_category_choice': variation_category_choice
    }
    return render(request, 'panel/variation/add-variation.html', context)
