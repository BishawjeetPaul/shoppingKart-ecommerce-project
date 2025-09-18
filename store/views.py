from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category


# This function is use for store.
def store(request, category_slug=None):
    categories      = None
    products        = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, isDelete=False)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(isDelete=False)

    categories = Category.objects.all().filter(isDelete=False)
    product_count = products.count()

    context = {
        'products': products,
        'categories': categories,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)
