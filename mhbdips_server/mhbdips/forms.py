from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import redirect, render
from .models import Review

from mhbdips.models import Account


class AccountRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=2)
    zipcode = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'address', 'city', 'state', 'zipcode')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            account = Account.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                address=self.cleaned_data['address'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                zipcode=self.cleaned_data['zipcode']
            )
        return user


class AccountLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


def UserChangeForm(request):
    user = request.user
    if request.method == 'POST':
        form = UserChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(request)

    return render(request, 'profile.html', {'form': form})


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Message', widget=forms.Textarea)


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        model = Review
        fields = ['rating', 'comments']


class CheckoutForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email', required=False)
    address = forms.CharField(label='Address', max_length=255)
    state = forms.CharField(label='State', max_length=100)
    zip_code = forms.CharField(label='ZIP Code', max_length=10)
    payment_method = forms.ChoiceField(choices=[('payment1', 'Payment Method 1'), ('payment2', 'Payment Method 2')])
    credit_card = forms.CharField(label='Credit Card', max_length=16)