from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(instance.title, reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return f'{instance.slug}/{filename}'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to=image_folder)
    available = models.BooleanField(default=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2,
                                     default=0.00)

    def __str__(self):
        return f'Cart item for product {self.product.title}'


class Cart(models.Model):
    items = models.ManyToManyField(CartItem)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2,
                                     default=0.00)

    def __str__(self):
        return str(self.id)

    def add_to_cart(self, product_slug):
        product = Product.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(product=product,
                                                     item_total=product.price)
        if new_item not in self.items.all():
            self.items.add(new_item)
            self.save()

    def remove_from_cart(self, product_slug):
        product = Product.objects.get(slug=product_slug)
        for cart_item in self.items.all():
            if cart_item.product == product:
                self.items.remove(cart_item)
                self.save()

    def change_qty(self, qty, item_id):
        cart_item = CartItem.objects.get(id=int(item_id))
        cart_item.qty = int(qty)
        cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
        cart_item.save()
        new_cart_total = 0.00
        for item in self.items.all():
            new_cart_total += float(item.item_total)
        self.cart_total = new_cart_total
        self.save()


ORDER_STATUS_CHOICES = (
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен'),
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    buying_type = models.CharField(max_length=100,
                                   choices=(('Самовывоз', 'Самовывоз'),
                                            ('Доставка', 'Доставка')),
                                   default='Самовывоз')
    date = models.DateField(auto_now_add=True)
    comments = models.TextField()
    status = models.CharField(max_length=200, choices=ORDER_STATUS_CHOICES,
                              default=ORDER_STATUS_CHOICES[0][0])

    def __str__(self):
        return f'Заказ №{self.id}'
