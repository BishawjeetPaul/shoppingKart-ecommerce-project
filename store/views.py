from store.models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator




# # This function is use for store.
# def store(request, category_slug=None):
#     # Base queryset
#     products = Product.objects.filter(isDelete=False)

#     # Filter by category if provided
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#     else:
#         products = products.order_by('id')

#     # Pagination
#     paginator = Paginator(products, 9)
#     page = request.GET.get('page')
#     paged_products = paginator.get_page(page)

#     # Categories for sidebar
#     categories = Category.objects.filter(isDelete=False)

#     context = {
#         'products': paged_products,
#         'categories': categories,
#         'product_count': products.count(),
#     }
#     return render(request, 'store/store.html', context)


def store(request, category_slug=None):
    products = Product.objects.filter(isDelete=False)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # IMPORTANT: add ordering before pagination
    products = products.order_by('id')

    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    categories = Category.objects.filter(isDelete=False)

    context = {
        'products': paged_products,
        'categories': categories,
        'product_count': products.count(),
    }
    return render(request, 'store/store.html', context)



# This function is use for product details.
def product_details(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    size_variations = single_product.variation_set.filter(variation_category='size')
    color_variations = single_product.variation_set.filter(variation_category='color')

    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'size_variations': size_variations,
        'color_variations': color_variations,
    }
    return render(request, 'store/product-details.html', context)


# This function is use for search products.
def search(request):
    products = Product.objects.none()   # safe empty queryset
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('created_at').filter(
                Q(product_description__icontains=keyword) | 
                Q(product_name__icontains=keyword)
            )
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request, 'store/store.html', context)