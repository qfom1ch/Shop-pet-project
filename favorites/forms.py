from django import forms

class FavoritesAddProductForm(forms.Form):
    qwe = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
