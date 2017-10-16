from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^meusemprestimos/$', views.MovimentacaoDeUsuarioListView.as_view(), name='meus-emprestimos'),
    url(r'^objetos/$', views.ObjetoListView.as_view(), name='objetos'),
    url(r'^objeto/(?P<pk>\d+)$', views.ObjetoDetailView.as_view(), name='objeto-detail'),
]

