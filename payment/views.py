from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product,Profile
import datetime 
# Create your views here.

def orders(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            if status == "true":
                order = Order.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(shipped=True,date_shipped=now)
                
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)

            messages.success(request,"Shippping Status Updated")
            return redirect('home')
                    

        return render(request,'payment/orders.html',{"order":order,"items":items}) 

    else:
        messages.success(request,"Access Denied")
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']

            messages.success(request,"Shipping Status Updated")
            return redirect('home')


        return render(request,"payment/not_shipped_dash.html",{"orders":orders})

    else:
        messages.success(request,"Access Denied")
        return redirect('home')

    

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']

            messages.success(request,"Shipping Status Updated")
            return redirect('home')
        return render(request,"payment/shipped_dash.html",{"orders":orders})

    else:
        messages.success(request,"Access Denied")
        return redirect('home')


def process_order(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
        return redirect('home')

    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    my_shipping = request.session.get('my_shipping')
    if not my_shipping:
        messages.error(request, "Shipping information is missing.")
        return redirect('cart')

    full_name = my_shipping.get('shipping_full_name', '')
    email = my_shipping.get('shipping_email', '')
    shipping_address = "\n".join([
        my_shipping.get('shipping_address1', ''),
        my_shipping.get('shipping_address2', ''),
        my_shipping.get('shipping_city', ''),
        my_shipping.get('shipping_state', ''),
        my_shipping.get('shipping_zipcode', ''),
        my_shipping.get('shipping_country', ''),
    ])

    amount_paid = totals
    user = request.user if request.user.is_authenticated else None

    # Create Order
    order = Order.objects.create(
        user=user,
        full_name=full_name,
        email=email,
        shipping_address=shipping_address,
        amount_paid=amount_paid
    )

    # Create Order Items
    for product in cart_products:
        product_id = product.id
        price = product.sale_price if product.is_sale else product.price
        quantity = quantities.get(str(product_id), 0)

        if quantity > 0:
            OrderItem.objects.create(
                order=order,
                product_id=product_id,
                user=user,
                quantity=quantity,
                price=price
            )

    # Clear session key and old cart
    request.session.pop('session_key', None)
    request.session.pop('my_shipping', None)

    if user:
        Profile.objects.filter(user=user).update(old_cart="")

    messages.success(request, "Order Placed")
    return redirect('home')




def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request,"payment/billing_info.html",{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_info":request.POST,"billing_form":billing_form})

        else:
            billing_form = PaymentForm()
            return render(request,"payment/billing_info.html",{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_form":request.POST,"billing_form":billing_form})

        shipping_form = request.POST
        return render(request,"payment/billing_info.html",{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_form":shipping_form})

    else:
        messages.success(request,"Access Denied")
        return redirect('home')



def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request,"payment/checkout.html",{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_form":shipping_form})
        

    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request,"payment/checkout.html",{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_form":shipping_form})



def payment_success(request):
    return render(request, "payment/payment_success.html",{})

