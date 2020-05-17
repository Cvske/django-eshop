from .models import *

def check_or_create_order(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_total_cart': 0, 'get_cart_items': 0}
            cartItems = order['get_cart_items']
        view_func(request, *args, **kwargs)

    return wrap


