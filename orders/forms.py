from django import forms

from orders.models import Order


class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'ул. Мира, дом 6, кв. 35',
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 9XX XXX XX XX'}))

    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Москва'}))

    postal_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXXXXX'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name','phone_number', 'email', 'city', 'address', 'postal_code')