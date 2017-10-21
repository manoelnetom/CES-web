from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^meusemprestimos/$', views.ReservaListView.as_view(), name='reserva'),
]

