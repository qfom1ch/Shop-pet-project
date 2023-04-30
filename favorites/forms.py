from django import forms


class FavoritesAddProductForm(forms.Form):
    product = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
