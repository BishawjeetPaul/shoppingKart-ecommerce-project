from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from store.models import Product, Variation
from carts.models import Cart, CartItem
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


# Private function.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# This function is use for item add-cart
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) # get the product
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            # print(key, value)

            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
                print(product_variation)
            except:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in th session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1 # cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    # redirect back to product detail page.
    return redirect(reverse('product-details', args=[product.category.slug, product.slug]))
    


# This function is use to add-cart-item
def add_cart_item(request, product_id):
    product = Product.objects.get(id=product_id) # get the product
    cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in th session

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1 # cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('cart')


# This function is use for cart page
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cgst = 0
        sgst = 0
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.quantity)
            quantity = cart_item.quantity

        # calculate total tax (5% of total amount)
        tax = (5 * total) / 100

        # split equally into SGST and CGST (2.5% each)
        sgst = tax / 2
        cgst = tax / 2

        grand_total = total + tax
            
    except ObjectDoesNotExist:
        pass # just ignore

    context = {
        'cgst': cgst,
        'sgst': sgst,
        'tax': tax,
        'grand_total': grand_total,
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    return render(request, 'carts/cart.html', context)


# This function is use for remove the product more than one in the cart
def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    # if card item greater than 1 
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


# This function is use for remove the item in the cart
def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')
