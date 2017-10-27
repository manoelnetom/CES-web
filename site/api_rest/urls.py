from django.conf.urls import url
from api_rest import views


app_name = 'api_rest'
urlpatterns = [
    url(r'^exibir_objetos/', views.ObjetosServiceView.as_view(), name='exibir_objetos'),
    url(r'^exibir_objeto/(?P<objeto_id>\d+)', views.ObjetoServiceView.as_view(), name='exibir_objeto'),
    url(r'^exibir_usuario/(?P<usuario_id>\d+)', views.UsuarioServiceView.as_view(), name='exibir_usuario'),
    url(r'^exibir_usuarios/', views.UsuariosServiceView.as_view(), name='exibir_usuarios'),
    url(r'^emprestar_objeto/', views.EmprestarObjetoServiceView.as_view(), name='emprestar_objeto'),
    url(r'^devolver_objeto/', views.DevolverObjetoServiceView.as_view(), name='devolver_objeto'),
    url(r'^transferir_objeto/', views.TransferirObjetoServiceView.as_view(), name='transferir_objeto'),
    url(r'^objetos_disponiveis/', views.ObjetoDisponivelServiceView.as_view(), name='objetos_disponiveis'),
    url(r'^movimentacoes_usuario/(?P<user_id>\d+)', views.MovimentacaoUsuarioServiceView.as_view(), name='movimentacoes_usuario'),
    url(r'^objetos_disponiveis_usuario/(?P<user_id>\d+)', views.ObjetoDisponivelUsuarioServiceView.as_view(), name='objetos_disponiveis_usuario'),
    url(r'^movimentacoes_abertas_usuario/(?P<user_id>\d+)', views.MovimentacaoAbertaUsuarioServiceView.as_view(), name='movimentacoes_abertas_usuario'),
    url(r'^detalhe_movimentacao/(?P<movimentacao_id>\d+)', views.DetalheMovimentacaoServiceView.as_view(), name='detalhe_movimentacao'),
    url(r'^filtro_movimentacoes_usuario/', views.FiltroMovimentacaoUsuarioServiceView.as_view(), name='filtro_movimentacao_usuario'),
    url(r'^confirmar_transferir_objeto/', views.ConfirmarTransferirObjetoServiceView.as_view(), name='confirmar_transferir_objeto'),
    url(r'^cancelar_transferir_objeto/', views.CancelarTransferirObjetoServiceView.as_view(), name='cancelar_transferir_objeto'),
    url(r'^listar_transferencias_usuario/', views.ListarTransferenciasUsuarioServiceView.as_view(), name='listar_transferencias_usuario'),
    url(r'^exibir_transferencia/', views.ExibirTransferenciaServiceView.as_view(), name='exibir_transferencia'),
    url(r'^solicitar_reserva/', views.SolicitarReservaServiceView.as_view(), name='solicitar_reserva'),
    url(r'^exibir_reservas_usuario/', views.ExibirReservasAbertasUsuarioServiceView.as_view(), name='exibir_reservas_usuario'),
    url(r'^cancelar_reserva/', views.CancelarReservaServiceView.as_view(), name='cancelar_reserva'),
    url(r'^status_objeto/', views.ObjectStatusListServiceView.as_view(), name='status_objeto'),    
]
