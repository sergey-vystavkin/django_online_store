from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .forms import LoginForm, OrderForm, RegistrationForm
from .models import Cart, CartItem, Category, Order, Product


def index_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category = Category.objects.get(id=5)
    products_for_carousel = Product.objects.filter(category=category)
    context = {
        'categories': categories,
        'products': products,
        'products_for_carousel': products_for_carousel,
    }
    return render(request, 'storeapp/index.html', context)


def category_view(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    categories = Category.objects.all()
    products_of_category = Product.objects.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products_of_category': products_of_category,
    }
    return render(request, 'storeapp/category.html', context)


def product_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
    }
    return render(request, 'storeapp/product.html', context)


def cart_object_creater(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    return cart


def cart_view(request):
    cart = cart_object_creater(request)
    categories = Category.objects.all()
    context = {
        'cart': cart,
        'categories': categories,
    }
    return render(request, 'storeapp/cart.html', context)


def add_to_cart_view(request):
    cart = cart_object_creater(request)
    product_slug = request.GET.get('product_slug')
    cart.add_to_cart(product_slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    request.session['total'] = cart.items.count()
    return JsonResponse({'cart_total': cart.items.count(),
                         'cart_total_price': cart.cart_total,
                         })


def remove_from_cart_view(request):
    cart = cart_object_creater(request)
    product_slug = request.GET.get('product_slug')
    cart.remove_from_cart(product_slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    request.session['total'] = cart.items.count()
    return JsonResponse({'cart_total': cart.items.count(),
                         'cart_total_price': cart.cart_total,
                         })


def change_item_qty(request):
    cart = cart_object_creater(request)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart.change_qty(qty, item_id)
    cart_item = CartItem.objects.get(id=int(item_id))
    return JsonResponse({'cart_total': cart.items.count(),
                         'item_total': cart_item.item_total,
                         'cart_total_price': cart.cart_total,
                         })


def checkout_view(request):
    cart = cart_object_creater(request)
    categories = Category.objects.all()
    context = {
        'cart': cart,
        'categories': categories,
    }
    return render(request, 'storeapp/checkout.html', context)


def create_order_view(request):
    cart = cart_object_creater(request)
    categories = Category.objects.all()
    form = OrderForm(request.POST or None)
    context = {
        'cart': cart,
        'categories': categories,
        'form': form,
    }
    return render(request, 'storeapp/order.html', context)


def make_order_view(request):
    cart = cart_object_creater(request)
    categories = Category.objects.all()
    form = OrderForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        buying_type = form.cleaned_data['buying_type']
        date = form.cleaned_data['date']
        address = form.cleaned_data['address']
        comments = form.cleaned_data['comments']
        Order.objects.create(
            user=request.user,
            items=cart,
            total=cart.cart_total,
            first_name=name,
            last_name=last_name,
            phone=phone,
            address=address,
            buying_type=buying_type,
            date=date,
            comments=comments,
        )
        del request.session['cart_id']
        del request.session['total']
        return render(request, 'storeapp/thank_you.html', {})
    return render(request, 'storeapp/order.html', {'categories': categories})


def account_view(request):
    order = Order.objects.filter(user=request.user).order_by('-id')
    categories = Category.objects.all()
    context = {
        'order': order,
        'categories': categories,
    }
    return render(request, 'storeapp/account.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('index'))
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'storeapp/login.html', context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.username = username
        new_user.save()
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('index'))
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'storeapp/registration.html', context)
