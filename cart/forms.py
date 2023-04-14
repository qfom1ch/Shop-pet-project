from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(label='')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CartAddProductFormWithoutChoice(forms.Form):
    quantity = forms.IntegerField(widget=forms.HiddenInput(), initial=1,)
    update = forms.BooleanField(required=False, initial=False,  widget=forms.HiddenInput())


class CartAddProductFormQuantity(forms.Form):
    quantity = forms.TypedChoiceField(label='', choices=BLANK_CHOICE_DASH + PRODUCT_QUANTITY_CHOICES, coerce=int,
                                      )
    update = forms.BooleanField(required=False, initial=True, widget=forms.HiddenInput)