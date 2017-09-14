from django.contrib import admin
from .models import TipoObjeto
from .models import Objeto
from .models import PerfilUsuario
from .models import Usuario
from .models import Movimentacao
from .models import Permissao_Objeto_x_Usuario
from .models import Permissao_Objeto_x_PerfilUsuario
from .models import AdminWeb

#para tornar models visível no site
admin.site.register(TipoObjeto)
admin.site.register(Objeto)
admin.site.register(PerfilUsuario)
admin.site.register(Usuario)
admin.site.register(Movimentacao)
admin.site.register(Permissao_Objeto_x_Usuario)
admin.site.register(Permissao_Objeto_x_PerfilUsuario)
admin.site.register(AdminWeb)
