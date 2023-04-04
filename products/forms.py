from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH


class SortForm(forms.Form):
    sort_form = forms.ChoiceField(label='', choices=BLANK_CHOICE_DASH + [
                                                        ('price', 'По возрастанию цены'),
                                                        ('-price', 'По убыванию цены')
                                                    ],
                                  widget=forms.Select(attrs={'class': 'form-control'}))
