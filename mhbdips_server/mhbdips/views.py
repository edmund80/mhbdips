from random import sample

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import generics
from django.contrib.auth.forms import UserChangeForm
from .forms import UserChangeForm, AccountLoginForm, AccountRegistrationForm, ContactForm
from .models import Product, OrderDetail, Shipper, Invoice, Review, ContactMessage
from .serializers import ProductSerializer, OrderDetailSerializer, \
    ShipperSerializer, InvoiceSerializer, ReviewSerializer


def home(request):
    product_5 = Product.objects.get(id=5)
    featured_products = Product.objects.filter(featured=True)
    return render(request, 'home.html', {'product': product_5, 'featured_products': featured_products})


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderDetailListCreateView(generics.ListCreateAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer


class OrderDetailRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer


class ShipperListCreateView(generics.ListCreateAPIView):
    queryset = Shipper.objects.all()
    serializer_class = ShipperSerializer


class ShipperRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipper.objects.all()
    serializer_class = ShipperSerializer


class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


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


def account_update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(instance=user)

    return render(request, 'profile.html', {'form': form})


def about_view(request):
    return render(request, 'about.html')


def cart_view(request):
    return render(request, 'cart.html')


def favorite(request):
    if request.user.is_authenticated:
        favorite_products = request.user.favorite_products.all()
    else:
        favorite_products = None
    return render(request, 'favorites.html', {'favorite_products': favorite_products})


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
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


def product_detail_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    random_products = sample(list(Product.objects.exclude(pk=product_id)), 3)
    print(random_products)  # Check the contents in your console
    return render(request, 'product_detail.html', {'product': product, 'random_products': random_products})
