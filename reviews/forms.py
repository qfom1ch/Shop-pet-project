from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH

from .models import Reviews


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""

    text = forms.CharField(label='', widget=forms.Textarea(attrs={
        'placeholder': "Оставьте отзыв...", 'cols': 115, 'rows': 5,
    }))

    image = forms.ImageField(label='', required=False)

    rating = forms.ChoiceField(label='Оценка:',
                               choices=BLANK_CHOICE_DASH + [
                                   (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')
                               ], required=True)

    class Meta:
        model = Reviews
        fields = ('user', 'text', 'image', 'rating')

        widgets = {'user': forms.HiddenInput()}
