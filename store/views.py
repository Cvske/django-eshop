import json, datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .forms import CreateUserForm, ProductForm, ProfileForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .decorators import check_or_create_order


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_total_cart': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    product_list = Product.objects.all()
    paginator = Paginator(product_list, 6)
    page = request.GET.get('page')


    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'cartItems': cartItems,
        'page_obj': products,
        'page': page,
    }
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_total_cart': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_total_cart':0, 'get_cart_items':0, 'shipping': False}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action: ', action)
    print('Product: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_total_cart:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in..')
    return JsonResponse('Payment submitted..', safe=False)


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username = form.cleaned_data.get('username'),
                                  password = form.cleaned_data.get('password1'))
            login(request, new_user)
            return redirect('store')

    context = {'form': form}
    return render(request, 'store/register.html', context)


def createProduct(request):
    form = ProductForm
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store')

    context = {'form': form}
    return render(request, 'store/order_form.html', context)

def editProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('store')

    context = {'form': form, 'product': product}
    return render(request, 'store/edit_form.html', context)


def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        product.delete()
        return redirect('store')

    context = {'product': product}
    return render(request, 'store/delete_product.html', context)


def search(request):
    query = request.GET.get('q')
    object_list = Product.objects.filter(name__icontains = query)

    context = {'products': object_list}
    return render(request, 'store/search.html', context)

@login_required(login_url='login')
def profile(request):
    customer = Customer.objects.get(id=request.user.customer.id)
    context = {'customer': customer}
    return render(request, 'store/profile.html', context)

@login_required(login_url='login')
def edit_profile(request):
    profile = Customer.objects.get(id=request.user.customer.id)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {'form': form}
    return render(request, 'store/edit_profile.html', context)


def show_products(request, category_name):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_total_cart': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']


    category = Category.objects.get(name=category_name)
    products = category.product_set.all()
    product_list = products
    paginator = Paginator(product_list, 6)
    page = request.GET.get('page')


    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)



    context = {'category': category,
               'products': products,
               'page_obj': products,
               'cartItems': cartItems,
               'page': page,
               }
    return render(request, 'store/show_products.html', context)