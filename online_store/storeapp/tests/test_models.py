from mixer.backend.django import mixer
import pytest

@pytest.fixture
def category(request, db):
    return mixer.blend('storeapp.Category')

@pytest.fixture
def product(request, db):
    return mixer.blend('storeapp.Product')


def test_category_get_absolute_url(category):
    url = '/category/' + category.slug + '/'
    absolute_url = category.get_absolute_url()
    assert url == absolute_url

def test_product_get_absolute_url(product):
    url = '/product/' + product.slug + '/'
    absolute_url = product.get_absolute_url()
    assert url == absolute_url