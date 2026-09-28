import os
import json
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Avg
from PIL import Image
from users.models import Country
from blog.models import Rate
from .models import Product, Brand, Category
from django.db import connection


def save_product_images(files):
    """Save original product images and their 100px/200px thumbnails."""
    save_folder = os.path.join(settings.MEDIA_ROOT, 'products')
    os.makedirs(save_folder, exist_ok=True)
    saved_images = []

    for file in files:
        filename = file.name.replace(' ', '_')
        base, ext = os.path.splitext(filename)
        ext = ext.lower()
        original_name = f'{base}{ext}'
        original_path = os.path.join(save_folder, original_name)

        with open(original_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        saved_images.append(f'products/{original_name}')

        with Image.open(original_path) as image:
            for size in (100, 200):
                thumbnail = image.copy()
                thumbnail.thumbnail((size, size))
                thumbnail_name = f'{size}_{original_name}'
                thumbnail.save(os.path.join(save_folder, thumbnail_name))
                saved_images.append(f'products/{thumbnail_name}')

    return saved_images


def update_user_view(request):
    user = request.user
    countries = Country.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        user.email = request.POST.get('email')
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        user.address = request.POST.get('address')
        user.country_id = request.POST.get('id_country')
        user.phone = request.POST.get('phone')
        user.avatar = request.FILES.get('avatar')
        user.save()
        return redirect('update_user_view')
    return render(request, 'update.html', {'countries': countries})


def my_product_view(request):
    products = Product.objects.filter(user=request.user).order_by('-create_date','-id')
    for product in products:
        product.display_image = next(
            (
                image for image in product.image
                if not os.path.basename(image).startswith(('100_', '200_'))
                and os.path.isfile(os.path.join(settings.MEDIA_ROOT, image))
            ),
            next(
                (
                    image for image in product.image
                    if os.path.isfile(os.path.join(settings.MEDIA_ROOT, image))
                ),
                None

            )
        )
    return render(request, 'my-product.html', {'products': products})

def  product_view(request):
        brands = Brand.objects.all()
        categories = Category.objects.all()

        if request.method == 'POST':
            name = request.POST.get('name')
            price = request.POST.get('price')
            category_id = request.POST.get('id_category')
            brand_id = request.POST.get('id_brand')
            status = request.POST.get('status', 0)
            sale = request.POST.get('sale', 0) if str(status) == '1' else 0
            company = request.POST.get('company', '')
            detail = request.POST.get('detail', '')
            files = request.FILES.getlist('image')
            error = {}

            if not files:
                error["image"] = "Phải chọn ít nhất 1 ảnh"
            elif len(files) > 3:
                error["image"] = "Chỉ tối đa 3 ảnh"
            else:
                for file in files:
                    if file.content_type not in ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']:
                        error["image"] = f"{file.name} không đúng định dạng hình ảnh (chỉ chấp nhận JPG, PNG)"
                        break
                    if file.size > 1 * 1024 * 1024:
                        error["image"] = f"{file.name} vượt quá 1 MB"
                        break
            if error:
                return JsonResponse({'status': 'error', 'error': error}, status=400)
            saved_filenames = save_product_images(files)
            Product.objects.create(
                user=request.user,
                name=name,
                price=price,
                id_category_id=category_id,
                id_brand_id=brand_id,
                status=status,
                sale=sale,
                company=company,
                image=saved_filenames,
                detail=detail
            )
            return JsonResponse({'success': True, 'message': 'Thêm sản phẩm thành công!', 'status': 'success'})

        return render(request, 'add-product.html', {
            'brands': brands,
            'categories': categories
        })

def edit_roduct_view(request, id):
    product = get_object_or_404(Product, id=id, user=request.user)
    original_images = [
        image for image in product.image
        if not os.path.basename(image).startswith(('100_', '200_'))
    ]

    if request.method == 'POST':
        delete_images = [
            image for image in request.POST.getlist('delete_images')
            if image in original_images
        ]
        new_files = request.FILES.getlist('image')
        remaining_images = [
            image for image in original_images
            if image not in delete_images
        ]
        error = {}

        if len(remaining_images) + len(new_files) > 3:
            error['image'] = 'Tổng số ảnh không được vượt quá 3'

        for file in new_files:
            if file.content_type not in [
                'image/jpeg', 'image/png', 'image/jpg', 'image/webp'
            ]:
                error['image'] = (
                    f'{file.name} không đúng định dạng hình ảnh '
                    '(chỉ chấp nhận JPG, PNG, WEBP)'
                )
                break
            if file.size > 1 * 1024 * 1024:
                error['image'] = f'{file.name} vượt quá 1 MB'
                break

        if error:
            return JsonResponse({'status': 'error', 'error': error}, status=400)

        files_to_delete = []
        for image in delete_images:
            folder, filename = os.path.split(image)
            files_to_delete.extend([
                image,
                os.path.join(folder, f'100_{filename}'),
                os.path.join(folder, f'200_{filename}'),
            ])

        for image in files_to_delete:
            image_path = os.path.join(settings.MEDIA_ROOT, image)
            if os.path.isfile(image_path):
                os.remove(image_path)

        product.image = [
            image for image in product.image
            if image not in files_to_delete
        ]

        product.image.extend(save_product_images(new_files))

        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.company = request.POST.get('company', '')
        product.detail = request.POST.get('detail', '')
        product.status = request.POST.get('status', 0)
        product.sale = request.POST.get('sale', 0)
        product.id_category_id = request.POST.get('id_category') or None
        product.id_brand_id = request.POST.get('id_brand') or None
        product.save()

        return redirect('my_product_view')

    return render(request, 'edit-product.html', {
        'product': product,
        'images': original_images,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
    })
def delete_product_view(request, id):
    product = get_object_or_404(
        Product,
        id=id,
        user=request.user
    )

    for image in product.image:
        image_path = os.path.join(settings.MEDIA_ROOT, image)
        if os.path.isfile(image_path):
            os.remove(image_path)

    product.delete()
    return redirect('my_product_view')

def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    images = product.image
    if isinstance(images, str):
        try:
            images = json.loads(images)
        except (TypeError, ValueError):
            images = [images]
    if not isinstance(images, list):
        images = []
    originals = [
        image for image in images
        if isinstance(image, str)
        and not os.path.basename(image).startswith(('100_', '200_'))
    ][:3]
    product.gallery_images = [
        {'name': image, 'url': settings.MEDIA_URL + image.lstrip('/\\')}
        for image in originals
    ]
    return render(request, 'product-detail.html', {
        'product': product,
    })

def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('id')
        qty = int(request.POST.get('qty', 1))
        if not product_id:
            return JsonResponse({'status': 'error', 'message': 'Không tìm thấy ID sản phẩm'}, status=400)
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, price, image FROM product_account_product  WHERE id = %s """, [product_id])
            row = cursor.fetchone()
        if not row:
            return JsonResponse({'status': 'error', 'message': 'Sản phẩm không tồn tại'}, status=404)
        image_data = row[3]
        if isinstance(image_data, str):
            try:
                image_data = json.loads(image_data)
            except:
                pass
        first_image = image_data[0] if isinstance(image_data, list) and len(image_data) > 0 else ""

        cart = request.session.get('cart', {})
        prod_key = str(product_id)
        if prod_key in cart:

            cart[prod_key]['quantity'] += qty
        else:
            cart[prod_key] = {
                'id': row[0],
                'name': row[1],
                'price': float(row[2]),
                'image': first_image,
                'quantity': qty
            }

        request.session['cart'] = cart
        total_quantity = sum(item['quantity'] for item in cart.values())
        request.session['cart_count'] = total_quantity
        request.session.modified = True

        return JsonResponse({
            'status': 'success',
            'product_id': product_id,
            'current_product_qty': cart[prod_key]['quantity'],
            'total_items': total_quantity
        })
    return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ'}, status=400)

    


def cart_view(request):


    return render(request, 'cart.html', {

    })
