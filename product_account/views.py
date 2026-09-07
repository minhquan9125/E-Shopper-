import os
import json
from django.shortcuts import render, redirect
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
    return render(request, 'my-product.html', {'products': products})

def product_view(request):
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