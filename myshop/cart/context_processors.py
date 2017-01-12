from .cart import Cart


def cart(request):
    """Inject the cart into all templates"""
    return {'cart': Cart(request)}
