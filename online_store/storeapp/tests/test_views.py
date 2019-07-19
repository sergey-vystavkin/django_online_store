from django.contrib.auth.models import User, AnonymousUser
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from storeapp.views import (index_view, category_view, product_view, cart_view,
                            checkout_view, create_order_view, make_order_view,
                            account_view, login_view)
import pytest

@pytest.mark.django_db
class TestViews:

    def test_index_view(self):
        path = reverse('index')
        request = RequestFactory().get(path)

        response = index_view(request)
        assert response.status_code == 200

    def test_category_view(self):
        mixer.blend('storeapp.Category', slug='test')
        path = reverse('category_detail', kwargs={'category_slug': 'test'})
        request = RequestFactory().get(path)

        response = category_view(request, 'test')
        assert response.status_code == 200

    def test_product_view(self):
        mixer.blend('storeapp.Product', slug='test')
        path = reverse('product_detail', kwargs={'product_slug': 'test'})
        request = RequestFactory().get(path)

        response = product_view(request, 'test')
        assert response.status_code == 200

    def test_cart_view(self):
        path = reverse('cart')
        request = RequestFactory().get(path)
        request.session = {}

        response = cart_view(request)
        assert response.status_code == 200

    def test_checkout_view(self):
        path = reverse('checkout')
        request = RequestFactory().get(path)
        request.session = {}

        response = checkout_view(request)
        assert response.status_code == 200

    def test_create_order_view(self):
        path = reverse('order')
        request = RequestFactory().get(path)
        request.session = {}

        response = create_order_view(request)
        assert response.status_code == 200

    def test_account_view(self):
        path = reverse('account')
        request = RequestFactory().get(path)
        request.session = {}
        request.user = mixer.blend(User)

        response = account_view(request)
        assert response.status_code == 200

    def test_login_view(self):
        path = reverse('login')
        request = RequestFactory().get(path)

        response = login_view(request)
        assert response.status_code == 200



