from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UsuarioNovoForm, UsuarioEdicaoForm
from .models import *

# para tornar models visível no portal do administrador
@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UsuarioEdicaoForm
    add_form = UsuarioNovoForm
    
    fieldsets = (
        ('Informações Pessoais', {'fields': ('matricula', 'nome', 'sobrenome', 'telefone', 'email',)}),
        ('Permissões', {'fields': ('is_admin', 'user_permissions',)}),
        ('Senha', {'fields': ('password',)}),
    )
    
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('matricula', 'email', 'nome', 'sobrenome', 'password1', 'password2',)}
        ),
    )
    
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('nome', 'sobrenome', 'telefone', 'email',)
    search_fields = ('matricula', 'nome', 'sobrenome',)
    list_filter = ()
    ordering = ('nome',)

@admin.register(Funcionario)
class FuncionarioAdmin(UsuarioAdmin):
    fieldsets = (
        ('Informações Pessoais', {'fields': ('matricula', 'nome', 'sobrenome', 'telefone', 'email', 'setor',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Senha', {'fields': ('password',)}),
    )
    
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a us
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('matricula', 'email','nome', 'sobrenome', 'password1', 'password2', 'setor',)}
        ),
    )
    
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('matricula', 'nome', 'sobrenome', 'setor',)
    list_filter = ('setor',)
    ordering = ('nome',)

@admin.register(Professor)
class ProfessorAdmin(UsuarioAdmin):
    fieldsets = (
        ('Informações Pessoais', {'fields': ('matricula', 'nome', 'sobrenome', 'telefone', 'email', 'departamento',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Senha', {'fields': ('password',)}),
    )
    
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('matricula', 'email','nome', 'sobrenome', 'password1', 'password2', 'departamento',)}
        ),
    )
    
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('matricula', 'nome', 'sobrenome', 'departamento',)
    list_filter = ('departamento',)
    ordering = ('nome',)

@admin.register(Aluno)
class AlunoAdmin(UsuarioAdmin):
    pass
    
admin.site.register(TipoObjeto)
admin.site.register(Objeto)
admin.site.register(Departamento)
admin.site.register(Setor)
admin.site.register(GrupoUsuario)
admin.site.register(GrupoObjeto)
admin.site.register(Movimentacao)