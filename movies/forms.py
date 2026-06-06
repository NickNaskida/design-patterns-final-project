from django import forms

from movies.models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "director", "release_year", "genre"]


class RatingForm(forms.Form):
    score = forms.DecimalField(
        min_value=0,
        max_value=10,
        max_digits=3,
        decimal_places=1,
        widget=forms.NumberInput(attrs={"step": "0.5", "min": "0", "max": "10"}),
    )