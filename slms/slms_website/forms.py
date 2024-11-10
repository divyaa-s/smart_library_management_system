from django import forms

class GenrePreferenceForm(forms.Form):
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('science_fiction', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('mystery', 'Mystery'),
        ('romance', 'Romance'),
        ('non_fiction', 'Non Fiction'),
        ('historical_fiction', 'Historical Fiction'),
        ('thriller', 'Thriller'),
        ('biography', 'Biography'),
        ('self_help', 'Self Help'),
    ]
    genres = forms.ChoiceField(choices=GENRE_CHOICES, required=False)
