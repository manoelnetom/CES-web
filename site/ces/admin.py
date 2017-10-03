from django.contrib import admin
from .models import *

#para tornar models visível no site
admin.site.register(TipoObjeto)
admin.site.register(Objeto)
admin.site.register(Movimentacao)
admin.site.register(Aluno)
admin.site.register(Professor)
admin.site.register(Funcionario)
admin.site.register(Departamento)
admin.site.register(Setor)
admin.site.register(Grupo)
admin.site.register(Permissao)









