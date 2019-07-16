from mixer.backend.django import mixer
import pytest

@pytest.mark.django_db
class TestModels:

    def test_category_get_absolute_url(self):
        product = mixer.blend('storeapp.Category')
        url = '/category/' + product.slug + '/'
        absolute_url = product.get_absolute_url()
        assert url == absolute_url

    def test_product_get_absolute_url(self):
        product = mixer.blend('storeapp.Product')
        url = '/product/' + product.slug + '/'
        absolute_url = product.get_absolute_url()
        assert url == absolute_url