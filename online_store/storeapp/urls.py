from django.contrib.auth.views import LogoutView
from django.urls import path, re_path, reverse_lazy

from .views import (account_view,  # qty_plus_view, qty_minus_view,
                    add_to_cart_view, cart_view, category_view,
                    change_item_qty, checkout_view, create_order_view,
                    index_view, login_view, make_order_view, product_view,
                    registration_view, remove_from_cart_view)

urlpatterns = [
    path('cart/', cart_view, name='cart'),
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('index')),
         name='logout'),
    path('account/', account_view, name='account'),
    path('make_order/', make_order_view, name='make_order'),
    path('order/', create_order_view, name='order'),
    path('checkout/', checkout_view, name='checkout'),
    re_path(r'remove_from_cart/', remove_from_cart_view,
            name='remove_from_cart'),
    re_path(r'add_to_cart/', add_to_cart_view, name='add_to_cart'),
    path('change_item_qty/', change_item_qty, name='change_item_qty'),
    path('category/<category_slug>/', category_view, name='category_detail'),
    path('product/<product_slug>/', product_view, name='product_detail'),
    path('', index_view, name='index'),
]
