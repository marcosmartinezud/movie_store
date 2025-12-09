from django import forms

from .models import Director, Movie


class MovieForm(forms.ModelForm):
    # Campo multiple para marcar uno o varios directores con checkboxes
    directors = forms.ModelMultipleChoiceField(
        queryset=Director.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-list'}),
    )

    class Meta:
        model = Movie
        fields = ['title', 'release_year', 'description', 'poster', 'genre', 'directors']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Ej. Inception'}),
            'release_year': forms.NumberInput(attrs={'class': 'input-control', 'placeholder': '2024'}),
            'description': forms.Textarea(
                attrs={'class': 'input-control textarea', 'rows': '4', 'placeholder': 'Sinopsis breve'}
            ),
            'poster': forms.URLInput(attrs={'class': 'input-control', 'placeholder': 'https://…'}),
            'genre': forms.Select(attrs={'class': 'input-control select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Carga los directores en cada request para evitar evaluarlos al importar el módulo
        self.fields['directors'].queryset = Director.objects.all().order_by('name')
