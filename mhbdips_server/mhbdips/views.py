from random import sample
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404
from .forms import AccountLoginForm, AccountRegistrationForm, ContactForm, ReviewForm, CheckoutForm, \
    CustomPasswordChangeForm
from .models import Product, OrderDetail, ContactMessage, Review


def home(request):
    product_5 = Product.objects.get(id=5)
    featured_products = Product.objects.filter(featured=True)
    return render(request, 'home.html', {'product': product_5, 'featured_products': featured_products})


def account_registration_view(request):
    if request.method == 'POST':
        form = AccountRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = AccountRegistrationForm()

    return render(request, 'register.html', {'form': form})


def account_login(request):
    if request.method == 'POST':
        form = AccountLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid login'})
    else:
        form = AccountLoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the profile page or another appropriate page
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'update_profile.html', {'form': form})


def about_view(request):
    return render(request, 'about.html')


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = OrderDetail.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.total_quantity for item in cart_items)

    form = CheckoutForm()
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            pass

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone', 'contact_method', 'best_time', 'message']


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def products_view(request):
    search_term = request.GET.get('search', '')
    if search_term:
        products = Product.objects.filter(name__icontains=search_term)
    else:
        products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


def product_detail_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    random_products = sample(list(Product.objects.exclude(pk=product_id)), 3)
    print(random_products)
    return render(request, 'product_detail.html', {'product': product, 'random_products': random_products})


def get_user_from_request(request):
    if request.user.is_authenticated:
        return request.user
    return None


@login_required
def add_to_order_details(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = Product.objects.get(id=product_id)
        total_price = product.price * quantity

        # Get the user info
        account = request.user.account

        # Create the order
        order_detail = OrderDetail.objects.create(
            user=request.user,
            name=f"{account.first_name} {account.last_name}",
            address=account.address,
            city=account.city,
            state=account.state,
            zipcode=account.zipcode,
            email=request.user.email,
            product=product,
            total_quantity=quantity,
            total_price=total_price,
            shipper=None
        )

    return render(request, 'products.html', {})


def add_review(request, product_id=None):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product_id = product_id
            review.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()

    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'reviews.html', {'form': form, 'product': product, 'reviews': reviews})


def update_cart_view(request, item_id):
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0:
            item = OrderDetail.objects.get(id=item_id)
            item.total_quantity = new_quantity
            item.save()
    return redirect('cart')


def remove_from_cart(request, item_id):
    try:
        order_detail = OrderDetail.objects.get(id=item_id)
        order_detail.delete()
        return redirect('cart')
    except OrderDetail.DoesNotExist:
        return redirect('cart')
