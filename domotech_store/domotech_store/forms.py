from django import forms
from django.contrib.auth.models import User
class RegisterForm(forms.Form):
    username = forms.CharField(required=True, min_length=4, max_length=50,
    #attrs atributos
    widget=forms.TextInput(attrs={
        'class':'form-control',
        'id':'username',
        'placeholder':'ingrese usuario'
    }))
    email = forms.EmailField(required=True,
    widget=forms.EmailInput(attrs={
        'class':'form-control',
        'id':'email',
        'placeholder':'ingrese correo'
    }))
    password = forms.CharField(required=True,
    widget=forms.PasswordInput(attrs={
        'class':'form-control',
    }))
    password2 = forms.CharField(label='Confirmar Password',required=True,
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
    }))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            #levantamos un error
            raise forms.ValidationError('El username ya se encuentra en uso')
        return username
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            #levantamos un error
            raise forms.ValidationError('El email ya se encuentra en uso')
        return email
    #Usaremos este metodo cuando tengamos campos q dependen de otros
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2','EL password no coincide')
    #crear un nuevo usuario
    def save(self):
        return User.objects.created_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )
