import os
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from users.models import CustomerUser
from .models import Product


@override_settings(MEDIA_ROOT=tempfile.mkdtemp(prefix='media_test_'))
class ProductImageEditTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomerUser.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='secret123',
        )
        self.product = Product.objects.create(
            user=self.user,
            name='Test product',
            price=100,
            image=['products/old1.jpg', 'products/old2.jpg'],
        )

    def test_edit_product_merges_existing_and_new_images(self):
        request = self.factory.post(
            reverse('edit_roduct_view', args=[self.product.id]),
            {
                'name': 'Updated product',
                'price': '150',
                'company': 'Acme',
                'detail': 'Nice product',
                'status': '0',
                'delete_images': ['products/old1.jpg'],
            }
        )
        request.user = self.user
        request.FILES['image'] = [
            SimpleUploadedFile('new1.jpg', b'fake-jpg-1', content_type='image/jpeg'),
            SimpleUploadedFile('new2.jpg', b'fake-jpg-2', content_type='image/jpeg'),
        ]

        response = self.client.post(
            reverse('edit_roduct_view', args=[self.product.id]),
            {
                'name': 'Updated product',
                'price': '150',
                'company': 'Acme',
                'detail': 'Nice product',
                'status': '0',
                'delete_images': ['products/old1.jpg'],
                'image': [
                    SimpleUploadedFile('new1.jpg', b'fake-jpg-1', content_type='image/jpeg'),
                    SimpleUploadedFile('new2.jpg', b'fake-jpg-2', content_type='image/jpeg'),
                ],
            },
            format='multipart',
        )

        self.product.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.product.image, ['products/old2.jpg', 'products/new1.jpg', 'products/new2.jpg'])

    def test_edit_product_rejects_more_than_three_images_after_merge(self):
        self.product.image = ['products/old1.jpg', 'products/old2.jpg']
        self.product.save(update_fields=['image'])

        response = self.client.post(
            reverse('edit_roduct_view', args=[self.product.id]),
            {
                'name': 'Updated product',
                'price': '150',
                'company': 'Acme',
                'detail': 'Nice product',
                'status': '0',
                'delete_images': [],
                'image': [
                    SimpleUploadedFile('new1.jpg', b'fake-jpg-1', content_type='image/jpeg'),
                    SimpleUploadedFile('new2.jpg', b'fake-jpg-2', content_type='image/jpeg'),
                ],
            },
            format='multipart',
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tối đa 3 ảnh')
