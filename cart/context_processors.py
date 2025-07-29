from .cart import Cart

# context processor to our cart to work on all pages
def cart(request):
    return {'cart':Cart(request)}