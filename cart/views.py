import json
import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from product_account.models import Product


def get_product_image(images):
    if isinstance(images, str):
        try:
            images = json.loads(images)
        except (TypeError, ValueError):
            images = [images]

    if not isinstance(images, list):
        return ''

    originals = [
        image for image in images
        if not os.path.basename(image).startswith(('100_', '200_'))
    ]

    for image in originals + images:
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, image)):
            return image

    return ''


def add_to_cart(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ'}, status=400)

    product_id = request.POST.get('id')
    if not product_id:
        return JsonResponse({'status': 'error', 'message': 'Không tìm thấy ID sản phẩm'}, status=400)

    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('qty', 1))
    cart = request.session.get('cart', {})
    product_id = str(product.id)

    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'image': get_product_image(product.image),
            'quantity': quantity,
        }

    request.session['cart'] = cart
    request.session['cart_count'] = cart_count(cart)

    return JsonResponse({
        'status': 'success',
        'product_id': product_id,
        'current_product_qty': cart[product_id]['quantity'],
        'total_items': request.session['cart_count'],
    })


def view_product_cart(request):
    cart = request.session.get('cart', {})

    for product_id, item in cart.items():
        product = Product.objects.filter(id=product_id).first()
        if product:
            item['image'] = get_product_image(product.image)
        item['total_price'] = item['quantity'] * item['price']

    total = sum(item['total_price'] for item in cart.values())
    return render(request, 'cart/cart.html', {
        'cart_items': cart.values(),
        'subtotal': total,
        'total': total,
    })


def cart_count(cart):
    return sum(item['quantity'] for item in cart.values())


def update_cart_view(request, id):
    cart = request.session.get('cart', {})
    product = cart[str(id)]
    action = request.POST.get('action')

    if action == 'up':
        product['quantity'] += 1
    elif action == 'down' and product['quantity'] > 1:
        product['quantity'] -= 1

    request.session['cart'] = cart
    request.session['cart_count'] = cart_count(cart)
    total = sum(item['quantity'] * item['price'] for item in cart.values())

    return JsonResponse({
        'success': True,
        'quantity': product['quantity'],
        'line_total': product['quantity'] * product['price'],
        'subtotal': total,
        'total': total,
        'cart_count': request.session['cart_count'],
    })


def delete_product_cart_view(request, id):
    cart = request.session.get('cart', {})
    del cart[str(id)]
    request.session['cart'] = cart
    request.session['cart_count'] = cart_count(cart)
    total = sum(item['quantity'] * item['price'] for item in cart.values())

    return JsonResponse({
        'success': True,
        'message': 'Product deleted',
        'cart_count': request.session['cart_count'],
        'subtotal': total,
        'total': total,
    })


def checkout_view(request):
    cart = request.session.get('cart', {})
    cart_items = []

    for product_id, item in cart.items():
        item['line_total'] = item['price'] * item['quantity']
        cart_items.append({**item, 'id': product_id})

    if not cart_items:
        return redirect('cart_view')

    total = sum(item['line_total'] for item in cart_items)
    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })
