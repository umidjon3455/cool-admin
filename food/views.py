import json

from django.shortcuts import render , redirect , resolve_url
from django.http import JsonResponse
from .models import *
from .services import *
from config.settings import MEDIA_ROOT
from .forms import *
def home_page(request):
    if request.GET:
        product = get_product_by_id(request.GET.get('product_id', 0))
        return JsonResponse(product)

def order_page(request):
    if request.GET:
        order = get_user_by_phone(request.GET.get('phone_number', 0))
        return JsonResponse(order)

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    orders = []
    order_list = request.COOKIES.get("orders")
    total_price = request.COOKIES.get("total_price", 0)
    print(total_price)
    print(order_list)
    if order_list:
        for key, val in json.loads(order_list).items():
            orders.index(
                {
                 "product": Product.objects.get(pk=int(key)),
                 "count": val
                }
            )
    ctx = {
        'categories':categories,
        'products':products,
        'orders':orders,
        'total_price':total_price
    }

    response = render(request, 'food/index.htm', ctx)
    response.set_cookie("getting", 'hello')
    return response

def main_order(request):
    if request.POST:
        try:
            model = Customer.objects.get(phone_number=request.POST.get('phone_number'))
        except:
            model = Customer()
        form = CustomerForm(request.POST or None, instance=model)
        if form.is_valid():
            customer = form.save()
            formOrder = OrderForm(request.POST or None, instance=Order)
            if formOrder.is_valid():
                order = formOrder.save(customer=customer)
                orders_list = request.COOKIES.get("orders")
                print("orders:",order)

            for key, value in json.loads(orders_list).items():
                product = get_product_by_id(int(key))

                counts = value
                order_product = OrderProduct(
                    count = counts,
                    price = product['price'],
                    product_id = product['id'],
                    order_id = order.id
                )
                order_product.save()

            return redirect('index')
        else:
            print(formOrder.errors)
