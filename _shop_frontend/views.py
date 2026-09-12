from django.shortcuts import render
import os
from django.conf import settings
from product_account.models import Product


def Home(request):
    products = Product.objects.all().order_by('-id')
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
    return render(request, 'Layout/base.html', {'products': products})


