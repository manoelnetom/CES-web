from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^reservas/$', views.ReservaListView.as_view(), name='reserva'),
    url(r'^reservas/add/(?P<pk>[0-9]+)/?$', views.FazerReservaView.as_view(), name='fazer_reserva'),
]
