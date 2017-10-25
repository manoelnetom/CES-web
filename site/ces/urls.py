from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^fazer_reserva/$', views.FazerReservaListView.as_view(), name='fazer_reserva'),
    url(r'^fazer_reserva/detalhe/(?P<pk>[0-9]+)/?$', views.ReservaCreateView.as_view(), name='reserva_new'),
]
