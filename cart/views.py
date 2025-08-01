from django.shortcuts import render,redirect, get_object_or_404
from .cart import Cart
from store.models import Product 
from django.http import JsonResponse 
from django.contrib import messages



# Create your views here.
def  cart_summary(request):
	cart = Cart(request)
	cart_products = cart.get_prods
	quantities = cart.get_quants
	totals = cart.cart_total()
	return render(request,"cart_summary.html",{"cart_products":cart_products,"quantities":quantities,"totals":totals})
    

def add_cart(request):
	# Get the cart
	cart = Cart(request)
	# test for POST
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		# lookup product in DB
		product = get_object_or_404(Product, id=product_id)
		
		# Save to session
		cart.add(product=product, quantity=product_qty)

		# Get Cart Quantity
		cart_quantity = cart.__len__()

		# Return resonse
		# response = JsonResponse({'Product Name: ': product.name})
		response = JsonResponse({'qty': cart_quantity})
		messages.success(request, ("Product Added To Cart..."))
		return response
    

def cart_delete(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		# Call delete Function in Cart
		cart.delete(product=product_id)

		response = JsonResponse({'product':product_id})
		#return redirect('cart_summary')
		messages.success(request, ("Item Deleted From Shopping Cart..."))
		return response
	
    



def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        # Validation
        if not product_id or not product_id.isdigit():
            return JsonResponse({'error': 'Invalid product ID'}, status=400)
        if not product_qty or not product_qty.isdigit():
            return JsonResponse({'error': 'Invalid quantity'}, status=400)

        product_id = int(product_id)
        product_qty = int(product_qty)

        # Update cart
        cart.update(product=product_id, quantity=product_qty)

        # Response
        messages.success(request, "Your Cart Has Been Updated...")
        return JsonResponse({'qty': product_qty})

		