from django.conf.urls import url
from api_rest import views


app_name = 'api_rest'
urlpatterns = [
    url(r'^exibir_objetos/', views.ObjetosServiceView.as_view(), name='exibir_objetos'),
    url(r'^exibir_objeto/(?P<objeto_id>\d+)', views.ObjetoServiceView.as_view(), name='exibir_objeto'),
    url(r'^emprestar_objeto/', views.EmprestarObjetoServiceView.as_view(), name='emprestar_objeto'),
    url(r'^devolver_objeto/', views.DevolverObjetoServiceView.as_view(), name='devolver_objeto'),
    url(r'^transferir_objeto/', views.TransferirObjetoServiceView.as_view(), name='transferir_objeto'),
    url(r'^objetos_disponiveis/', views.ObjetoDisponivelServiceView.as_view(), name='objetos_disponiveis'),
    url(r'^movimentacoes_usuario/(?P<user_id>\d+)', views.MovimentacaoUsuarioServiceView.as_view(), name='movimentacoes_usuario'),
    url(r'^objetos_disponiveis_usuario/(?P<user_id>\d+)', views.ObjetoDisponivelUsuarioServiceView.as_view(), name='objetos_disponiveis_usuario'),
    url(r'^movimentacoes_abertas_usuario/(?P<user_id>\d+)', views.MovimentacaoAbertaUsuarioServiceView.as_view(), name='movimentacoes_abertas_usuario'),
]
