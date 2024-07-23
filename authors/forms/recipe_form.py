from django import forms
from recipes.models import Recipe
from django.core.exceptions import ValidationError
from utils.django_forms import add_widget_attr

class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_widget_attr(self.fields.get('preparation_steps'), 'class', 'col-md-12')

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'preparation_time', 'preparation_time_unit', 'servings', 'servings_unit',
                    'preparation_steps', 'cover'  
                ]

        labels = {
            'title': 'Titulo',
            'description': 'Descrição',
            'preparation_time': 'Tempo de preparo',
            'preparation_time_unit': 'Tempo',
            'servings': 'Quantidade de pessoas servidas',
            'servings_unit': 'Forma de servir',
            'preparation_steps': 'Modo de preparo',
            'cover': 'Imagem',
        }

        widgets = {
            'cover': forms.FileInput(attrs={'class': 'col-md-12'}),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                )
            )
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            raise ValidationError('O título deve ter no minímo 5 caracteres', code='min_length')
        
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')

        if len(description) < 5:
            raise ValidationError('A descrição deve ter no minímo 5 caracteres', code='min_length')
        
        return description

    def clean_servings(self):
        servings = int(self.cleaned_data.get('servings'))

        if servings < 1:
            raise ValidationError(
                'Precisa servir no mínimo 1 pessoa',
                code='invalid'
            )
        
        return servings
        
    def clean(self):
        data = super().clean()

        preparation_time = int(self.cleaned_data.get('preparation_time'))
        preparation_time_unit = self.cleaned_data.get('preparation_time_unit')

        if preparation_time < 5 and preparation_time_unit == 'Minutos':
            raise ValidationError({
                'preparation_time': 'O tempo de preparo deve ter no mínimo 5 minutos'
            }, code='invalid')
        
        return data
    