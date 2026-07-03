from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Cart, Category, Item, Order, OrderItem
from .forms import LoginForm
from django.http import HttpResponse, HttpRequest


def login_view(request: HttpRequest) -> HttpResponse:
    '''a view that handles the login process'''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect('main_page')
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})


@login_required
def main_page_view(request: HttpRequest) -> HttpResponse:
    '''a simple main page view that renders itself when user is logged in'''
    categories = Category.objects.all()
    items = Item.objects.all()
    context = {
        'categories': categories,
        'items': items
    }
    return render(request, 'main.html', context)


@login_required
@require_POST
def buy_item_view(request: HttpRequest, item_id: int) -> HttpResponse:
    '''a view that creates an order from the selected item'''
    item = get_object_or_404(Item, id=item_id)
    order = Order.objects.create(
        user=request.user,
        total_price=item.price,
    )
    OrderItem.objects.create(
        order=order,
        item=item,
        price=item.price,
        quantity=1,
    )

    return redirect('my_orders')


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    '''a view that renders the profile page'''
    orders_count = request.user.orders.count()
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items_count = cart.items.count()

    context = {
        'profile_user': request.user,
        'orders_count': orders_count,
        'cart_items_count': cart_items_count,
    }
    return render(request, 'profile.html', context)


@login_required
def my_orders_view(request: HttpRequest) -> HttpResponse:
    '''a view that renders the my orders page'''
    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related('items__item')
        .order_by('-created_at')
    )
    return render(request, 'my_orders.html', {'orders': orders})


@login_required
def cart_view(request: HttpRequest) -> HttpResponse:
    '''a view that renders the cart page'''
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('item')

    total_price = 0
    for cart_item in cart_items:
        cart_item.line_total = cart_item.item.price * cart_item.quantity
        total_price += cart_item.line_total

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


@login_required
def settings_view(request: HttpRequest) -> HttpResponse:
    '''a view that renders the settings page'''
    return render(request, 'settings.html', {'profile_user': request.user})


def logout_view(request: HttpRequest) -> HttpResponse:  
    '''a view that handles the logout process'''
    logout(request)
    return redirect('login')