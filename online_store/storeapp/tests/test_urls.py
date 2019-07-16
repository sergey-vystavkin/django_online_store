from django.urls import resolve, reverse


class TestUrls:

    def test_cart_url(self):
        path = reverse('cart')
        assert resolve(path).view_name == 'cart'

    def test_registration_url(self):
        path = reverse('registration')
        assert resolve(path).view_name == 'registration'

    def test_login_url(self):
        path = reverse('login')
        assert resolve(path).view_name == 'login'

    def test_logout_url(logout):
        path = reverse('logout')
        assert resolve(path).view_name == 'logout'

    def test_account_url(self):
        path = reverse('account')
        assert resolve(path).view_name == 'account'

    def test_make_order_url(self):
        path = reverse('make_order')
        assert resolve(path).view_name == 'make_order'

    def test_order_url(self):
        path = reverse('order')
        assert resolve(path).view_name == 'order'

    def test_checkout_url(self):
        path = reverse('checkout')
        assert resolve(path).view_name == 'checkout'

    def test_remove_from_cart_url(self):
        path = reverse('remove_from_cart')
        assert resolve(path).view_name == 'remove_from_cart'

    def test_add_to_cart_url(self):
        path = reverse('add_to_cart')
        assert resolve(path).view_name == 'add_to_cart'

    def test_change_item_qty_url(self):
        path = reverse('change_item_qty')
        assert resolve(path).view_name == 'change_item_qty'

    def test_index_url(self):
        path = reverse('index')
        assert resolve(path).view_name == 'index'


