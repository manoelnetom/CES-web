# coding=utf-8
from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UsuarioNovoForm, UsuarioEdicaoForm
from .models import *

# para tornar models visível no portal do administrador

class MembersInline(admin.TabularInline):
    model = MemberGrupoUsuario
    extra = 1

class UsuarioAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UsuarioEdicaoForm
    add_form = UsuarioNovoForm

    fieldsets = (
        ('Informações Pessoais', {'fields': ('matricula', 'nome', 'sobrenome', 'telefone', 'email',)}),
        ('Permissões', {'fields': ('user_permissions',)}),
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

    inlines = (MembersInline,)
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
        ('Permissions', {'fields': ('user_permissions',)}),
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
        ('Permissions', {'fields': ('user_permissions',)}),
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


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    search_fields = ('descricao',)
    ordering = ('descricao',)


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    search_fields = ('descricao',)
    ordering = ('descricao',)


@admin.register(Objeto)
class ObjetoAdmin(admin.ModelAdmin):
    list_display = ('codigo','nome', 'tipoObjeto')
    list_filter = ('tipoObjeto',)
    search_fields = ('codigo', 'nome')
    ordering = ('nome',)


@admin.register(TipoObjeto)
class TipoObjetoAdmin(admin.ModelAdmin):
   list_display = ('nome',)
   search_fields = ('nome',)
   ordering = ('nome',)


@admin.register(GrupoObjeto)
class GrupoObjetoAdmin(admin.ModelAdmin):
   list_display = ('descricao', 'ativo','dataCriacao',)
   search_fields = ('descricao',)
   ordering = ('descricao',)


@admin.register(GrupoUsuario)
class GrupoUsuarioAdmin(admin.ModelAdmin):
   inlines = (MembersInline,)
   list_display = ('descricao','ativo','dataCriacao',)
   search_fields = ('descricao',)
   ordering = ('descricao',)


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('objeto' ,'status', 'usuario')
    list_filter = ('status',)
    search_fields = ('objeto__nome', 'usuario__nome', 'objeto__tipoObjeto__nome')
    ordering = ('objeto__nome',)

    actions = ['confirmar_retirada', 'confirmar_devolucao']

    def confirmar_retirada(self, request, queryset):
        queryset.update(status='2', retirada=timezone.now)
    confirmar_retirada.short_description = "Marcar objeto como emprestado"

    def confirmar_devolucao(self, request, queryset):
        queryset.update(status='4',devolucao=timezone.now)
    confirmar_devolucao.short_description = "Marcar objeto como devolvido"
