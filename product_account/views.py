import os
import json
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from PIL import Image
from users.models import Country
from .models import Product, Brand, Category

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
    products = Product.objects.filter(user=request.user).order_by('-id')
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
            saved_filenames = []
            save_folder = os.path.join(settings.MEDIA_ROOT, "products")
            os.makedirs(save_folder, exist_ok=True)

            for file in files:
                filename = file.name.replace(" ", "_")
                base, ext = os.path.splitext(filename)
                ext = ext.lower()

                original_path = os.path.join(save_folder, f"{base}{ext}")

                with open(original_path, "wb+") as dest:
                    for chunk in file.chunks():
                        dest.write(chunk)

                saved_filenames.append(f"products/{base}{ext}")

                img = Image.open(original_path)
                for size in [100, 200]:
                    img_copy = img.copy()
                    img_copy.thumbnail((size, size))
                    resized_name = f"products/{size}_{base}{ext}"
                    resized_path = os.path.join(settings.MEDIA_ROOT, resized_name)
                    img_copy.save(resized_path)
                    saved_filenames.append(resized_name)
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

        save_folder = os.path.join(settings.MEDIA_ROOT, 'products')
        os.makedirs(save_folder, exist_ok=True)
        for file in new_files:
            filename = file.name.replace(' ', '_')
            base, ext = os.path.splitext(filename)
            ext = ext.lower()
            original_path = os.path.join(save_folder, f'{base}{ext}')

            with open(original_path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)

            product.image.append(f'products/{base}{ext}')
            img = Image.open(original_path)
            for size in [100, 200]:
                img_copy = img.copy()
                img_copy.thumbnail((size, size))
                resized_name = f'products/{size}_{base}{ext}'
                resized_path = os.path.join(settings.MEDIA_ROOT, resized_name)
                img_copy.save(resized_path)
                product.image.append(resized_name)

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

