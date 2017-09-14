from django.conf.urls import url
from api_rest import views


app_name = 'api_rest'
urlpatterns = [
    url(r'^movimentacoes_aberto/(?P<user_id>\d+)', views.MovimentacaoAbertoServiceView.as_view(), name='movimentacoes_aberto'),
    url(r'^devolver_objeto/', views.DevolverObjetoServiceView.as_view(), name='devolver_objeto'),
]
