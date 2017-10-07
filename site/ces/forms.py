from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Usuario


class UsuarioNovoForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UsuarioNovoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Usuario
        fields = ('matricula', 'email', 'nome', 'sobrenome',)
        

class UsuarioEdicaoForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UsuarioEdicaoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Usuario
        fields = ('matricula', 'email', 'nome', 'sobrenome',)