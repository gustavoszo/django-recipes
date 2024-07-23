from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder

class RegisterForm(forms.ModelForm):
    
    # Usar o init da classe para ao invés de sobreescrever um campo ou suas informações, apenas adicionar algo nele
    def __init__(self, *args, **kwargs):
        # A classe base Form tem seu próprio __init__ que configura internamente vários atributos importantes do formulário, como os campos e widgets. Se não chamar o super().__init__(*args, **kwargs), essas inicializações não ocorrerão corretamente
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['first_name'], 'Digite seu primeiro nome')
        add_placeholder(self.fields['last_name'], 'Digite seu último nome')
        add_placeholder(self.fields['username'], 'Digite seu nome de usuário')
        add_placeholder(self.fields['email'], 'Digite seu e-mail')
    
    confirm_password = forms.CharField(
        required=True,
        label='Confirmação de senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha'
        })
    )
     
    class Meta:
        model= User
        fields= ['first_name', 'last_name', 'username', 'email', 'password']

        # Por padrão já estavam esse labels (field name com inicial maiúscula)
        labels = {
            'first_name': 'Primeiro nome',
            'last_name': 'Último nome',
            'username': 'Username',
            'email': 'Endereço de e-mail',
            'password': 'Senha',
        }

        help_texts = {
            'email': 'O endereço de e-mail precisa ser válido'
        }

        error_messages = {
            'username': {
                'required': 'Este campo precisa ser preenchido',
                # 'max_length': 'O username deve ter o máximo de X caracteres'
                'invalid': 'Valor inválido'
            }
        }

        # Cada campo tem um widget especifico (CSS, Input Type, Placeholder..)
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Digite seu primeiro nome',
                # 'class': 'form-control'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Digite sua senha'
            }),
        }

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'atencao' in data:
            raise ValidationError(
                # O 's' de %() é de string
                'Não digite %(value)s no first_name',
                code = 'invalid',
                params = {'value': 'atencao'}
            )

        return data
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError('Esse endereço de e-mail já está cadastrado.', code='invalid')
        
        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError({
                'confirm_password': 'As senhas precisam ser iguais',
            }, code='invalid')
            