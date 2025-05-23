from django import forms
from .models import FavoriteFlight


class FavoriteFlightForm(forms.ModelForm):
    class Meta:
        model = FavoriteFlight
        fields = ['liked', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Añade un comentario...'}),
            'liked': forms.CheckboxInput(),
        }
        labels = {
            'liked': 'Me gusta',
            'comment': 'Comentario',
        }
