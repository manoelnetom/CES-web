from django.shortcuts import render

from django.views import generic

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Objeto, Movimentacao


@login_required
def index(request):
    
    
    pendentes = Movimentacao.objects.filter(usuario=request.user, retirada__isnull=False, devolucao__isnull=True)
    
    reservados = Movimentacao.objects.filter(usuario=request.user, retirada__isnull=True)

    return render(
        request,
        'index.html',
        context={' reservados':  reservados, 'pendentes' : pendentes },
    )


class ReservaListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.    """
   
    model = Objeto
    template_name = 'ces/reserva.html'
    paginate_by = 10    

    def get_queryset(self):
        
      return Objeto.objects.all()

