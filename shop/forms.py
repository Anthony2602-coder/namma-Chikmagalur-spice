from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Address, Review, Newsletter


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "full_name", "phone", "address_line1", "address_line2",
            "city", "state", "pincode", "is_default",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full Name"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "address_line1": forms.TextInput(attrs={"class": "form-control", "placeholder": "Address Line 1"}),
            "address_line2": forms.TextInput(attrs={"class": "form-control", "placeholder": "Address Line 2 (optional)"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}),
            "pincode": forms.TextInput(attrs={"class": "form-control", "placeholder": "Pincode"}),
            "is_default": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "title", "comment"]
        widgets = {
            "rating": forms.Select(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(5, 0, -1)], attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Review title"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Share your experience..."}),
        }


class CheckoutForm(forms.Form):
    shipping_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    shipping_phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={"class": "form-control"}))
    shipping_address = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}))
    shipping_city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    shipping_state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    shipping_pincode = forms.CharField(max_length=10, widget=forms.TextInput(attrs={"class": "form-control"}))
    payment_method = forms.ChoiceField(
        choices=[("cod", "Cash on Delivery"), ("upi", "UPI"), ("card", "Credit/Debit Card")],
        widget=forms.RadioSelect(attrs={"class": "payment-radio"}),
    )
    coupon_code = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Coupon code"}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Order notes (optional)"}))


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"}),
        }


class ProductSearchForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "search-input", "placeholder": "Search coffee, pepper..."}))
    category = forms.CharField(required=False)
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ("", "Featured"),
            ("price_low", "Price: Low to High"),
            ("price_high", "Price: High to Low"),
            ("rating", "Customer Rating"),
            ("newest", "Newest Arrivals"),
        ],
    )
