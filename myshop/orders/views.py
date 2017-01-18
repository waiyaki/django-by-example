from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from cart.cart import Cart
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order, product=item['product'],
                    price=item['price'], quantity=item['quantity']
                )

            cart.clear()
            # launch async task
            order_created.delay(order.id)
            request.session['order_id'] = order.id  # set the order in the session
            return redirect(reverse('payment:process'))  # redirect to the payment.
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    context = {'cart': cart, 'form': form}
    return render(request, 'orders/order/create.html', context)