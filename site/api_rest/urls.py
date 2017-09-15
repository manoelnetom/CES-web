from django.conf.urls import url
from api_rest import views


app_name = 'api_rest'
urlpatterns = [
    url(r'^movimentacao_aberta/(?P<user_id>\d+)', views.MovimentacaoAbertaServiceView.as_view(), name='movimentacoes_aberto'),
    url(r'^devolver_objeto/', views.DevolverObjetoServiceView.as_view(), name='devolver_objeto'),
    url(r'^exibir_objetos/', views.ObjetoServiceView.as_view(), name='exibir_objetos'),
]
