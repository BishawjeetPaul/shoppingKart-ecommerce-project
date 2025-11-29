from django.shortcuts import render, get_object_or_404, redirect
from category.models import Category
from store.models import Product, Variation
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from store.models import variation_category_choice   # if you store choices her




# This function for admin-customization.
def admin_panel(request):
    return render(request, 'admin-panel.html')

# --------------------CATEGORY-FUNCTIONS------------------ #

# This function for add category
def add_category(request):
    if request.method == 'POST':
        try:
            category_name = request.POST.get('category_name')
            category_description = request.POST.get('category_description')
            category_image = request.FILES.get('category_image')
            
            categories = Category.objects.create(
                category_name=category_name,
                category_description=category_description,
                category_image=category_image
            )
            categories.save()
            messages.success(request, "Category Added Successfully")
            return redirect('add-category')
        except Exception as e:
            messages.error(request, "Failed to Added category. Something went wrong")
            return redirect('add-category')
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

            messages.success(request, "Category Updated Successfully")
            return redirect('manage-category')  # ✅ redirect instead of HttpResponseRedirect

        except Exception as e:
            messages.error(request, "Failed to update category. Something went wrong")
            return redirect('edit-category', category_id=category.id)  # ✅ redirect back to edit page

    return render(request, 'panel/category/edit-category.html', context)


# This function is use for delete category
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    try:
        category.isDelete=True
        category.save()
        messages.success(request, "Category deleted successfully!")
    except:
        messages.error(request, "Something went wrong. Could not delete category.")
    return redirect('manage-category')

# --------------------PRODUCT-FUNCTIONS------------------- #

# This function for add products.
def add_product(request):
    categories = Category.objects.filter(isDelete=False)
    context = {'categories': categories}

    if request.method == 'POST':
        try:
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
            messages.success(request, "Product Added Successfully")
            return redirect('add-product')
        except Exception as e:
            messages.error(request, "Faild to Added product. Something went wrong")
            return redirect('add-product')

        # Optional: redirect after success
        # return redirect('manage_products')  

    return render(request, 'panel/products/add-products.html', context)


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
    return render(request, 'panel/products/manage-products.html', context)


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
    return render(request, 'panel/products/manage-products.html', context)


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

            messages.success(request, "Product Updated Successfully")
            return redirect('manage-product')  # ✅ redirect instead of HttpResponseRedirect

        except Exception as e:
            messages.error(request, "Failed to update product. Something went wrong")
            return redirect('edit-product', product_id=product.id)  # ✅ redirect back to edit page
            # return redirect('manage-product')
    return render(request, 'panel/products/edit-product.html', context)


# This function for delete-product.
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        product.isDelete=True
        product.save()
        messages.success(request, "Product deleted successfully!")
    except:
        messages.error(request, "Something went wrong. Could not delete product.")
    return redirect('manage-product')

# -----------------------VARIATION------------------------ #

# Variation category choices
variation_category_choice = (
    ('color', 'color'),
    ('size', 'size')
)


# This function for add-variations
def add_variation(request):
    products = Product.objects.filter(isDelete=False)
    variations = Variation.objects.all().order_by('-created_at')

    if request.method == 'POST':
        try:
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
            messages.success(request, "Variation Added Successfully")
            return redirect('add-variation')
        except Exception as e:
            messages.error(request, "Failed Add something went wrong")
            return redirect('add-variation')
    context = {
        'products': products,
        'variations': variations,
        'variation_category_choice': variation_category_choice
    }
    return render(request, 'panel/variation/add-variation.html', context)


# This function for manage-variation
def manage_variation(request):
    # Filter Colors & Size Separately
    color_variations = Variation.objects.filter(variation_category="color", isDelete=False).order_by('id')
    size_variations = Variation.objects.filter(variation_category='size', isDelete=False).order_by('id')

    # Paginate both tables (Optional)
    color_paginator = Paginator(color_variations, 10)
    size_paginator = Paginator(size_variations, 10)

    color_page = request.GET.get('color_page')
    size_page = request.GET.get('size_page')

    color_variations = color_paginator.get_page(color_page)
    size_variations = size_paginator.get_page(size_page)

    # variations = Variation.objects.filter(is_active=False).order_by('id')
    # paginator = Paginator(variations, 10)
    # page = request.GET.get('page')
    # variations = paginator.get_page(page)
    context = {
        'color_variations': color_variations,
        'size_variations': size_variations
    }
    return render(request, 'panel/variation/manage-variation.html', context)


# This function for search-color-variation.
def search_color_variation(request):
    # Base QuerySets
    color_variations = Variation.objects.filter(variation_category="color", isDelete=False).order_by('id')
    color_variation_count = 0

    keyword1 = request.GET.get('keyword1', '').strip()

    if keyword1:
        color_variations = color_variations.filter(
            Q(product__product_name__icontains=keyword1) |
            Q(variation_value__icontains=keyword1)
        )
        color_variation_count = color_variations.count()

    # Pagination AFTER search
    color_paginator = Paginator(color_variations, 10)
    color_page = request.GET.get('color_page')
    color_variations = color_paginator.get_page(color_page)

    context = {
        'color_variation_count': color_variation_count,
        'color_variations': color_variations,
        'keyword1': keyword1           
    }
    return render(request, 'panel/variation/manage-variation.html', context)


# This function for search-size-variation.
def search_size_variation(request):
    # Base QuerySets
    size_variations = Variation.objects.filter(variation_category="size", isDelete=False).order_by('id')
    size_variation_count = 0

    keyword2 = request.GET.get('keyword2', '').strip()

    if keyword2:
        size_variations = size_variations.filter(
            Q(product__product_name__icontains=keyword2) |
            Q(variation_value__icontains=keyword2)
        )
        size_variation_count = size_variations.count()

    # Pagination AFTER search
    size_paginator = Paginator(size_variations, 10)
    size_page = request.GET.get('size_page')
    size_variations = size_paginator.get_page(size_page)

    context = {
        'size_variation_count': size_variation_count,
        'size_variations': size_variations,
        'keyword2': keyword2           
    }
    return render(request, 'panel/variation/manage-variation.html', context)

# This function for edit-variation
def edit_variation(request, variation_id):
    variation = get_object_or_404(Variation, id=variation_id)
    products = Product.objects.filter(isDelete=False).order_by('product_name')
    context = {
        'variation': variation,
        'products': products,
        'variation_category_choice': variation_category_choice
    }
    
    if request.method == 'POST':
        product_id          = request.POST.get('product')
        variation_category  = request.POST.get('variation_category')
        variation_value     = request.POST.get('variation_value')
        is_active           = request.POST.get('is_active') == 'on'

        try:
            variation.variation_category=variation_category
            variation.variation_value=variation_value
            variation.is_active=is_active
            product = Product.objects.get(id=product_id)
            variation.product_id=product
            # Update Variation model
            variation.save()

            messages.success(request, "Variation Updated Successfully")
            return redirect('manage-variation')  # ✅ redirect instead of HttpResponseRedirect
        except Exception as e:
            messages.error(request, "Failed to Update something went wrong")
            return redirect('edit-variation', variation_id=variation.id)  # ✅ redirect back to edit page
    return render(request, 'panel/variation/edit-variation.html', context)


# This function for delete-variation
def delete_variation(request, variation_id):
    variation = Variation.objects.get(id=variation_id)
    try:
        variation.isDelete=True
        variation.save()
        messages.success(request, "Variation deleted successfully!")
    except:
        messages.error(request, "Something went wrong. Could not delete variation.")
    return redirect('manage-variation')

