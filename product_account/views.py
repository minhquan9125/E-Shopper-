from django.shortcuts import render,redirect
from users.models import Country
from .models import Product
import json
 
def update_user_view(request):
    user = request.user
    countries = Country.objects.all()
    if request.method == 'POST':
        username=request.POST.get('username')
        user.email=request.POST.get('email')
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        user.address=request.POST.get('address')
        user.country_id=request.POST.get('id_country')
        user.phone=request.POST.get('phone')
        user.avatar=request.FILES.get('avatar')
        user.save()
        return redirect('update_user_view')
    return render(request, 'update.html', {'countries': countries})


def product_view(request):
    user_products = Product.objects.filter(user=request.user)
    
    for product in user_products:
        if product.image:
            image_value = product.image.strip()
            try:
                images = json.loads(image_value)
            except json.JSONDecodeError:
                images = image_value

            if isinstance(images, list):
                product.first_image = images[0] if images else ''
            else:
                product.first_image = images
    return render(request,'my-product.html',{'products' : user_products})                       