from django.shortcuts import render, get_object_or_404

from django.views import generic

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.template.loader import render_to_string

from .models import Objeto, Movimentacao, GrupoObjeto, STATUS_OBJETO


@login_required
def index(request):
    
    pendentes = Movimentacao.objects.filter(usuario__matricula=request.user.matricula ).exclude(retirada__isnull=True).exclude(devolucao__isnull=False)
    reservados = Movimentacao.objects.filter(usuario__matricula=request.user.matricula).exclude(retirada__isnull=False)

    return render(
        request,
        'reserva_dashboard.html',
        context={'reservados':  reservados, 'pendentes' : pendentes },
    )


class FazerReservaListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing ojects on loan to current user.    """
   
    model = Objeto
    template_name = 'ces/fazer_reserva.html'
    paginate_by = 10    

    def get_queryset(self):
        objetos_acessiveis = GrupoObjeto.objects.filter(grupousuario__usuarios__matricula=self.request.user.matricula).values('objetos__id')
        objetos_pendentes_ou_reservados = Movimentacao.objects.filter(usuario__matricula=self.request.user.matricula 
                                                                     ).exclude(devolucao__isnull=False).values('objeto_id')
          
        return Objeto.objects.filter(id__in=objetos_acessiveis).exclude(id__in=objetos_pendentes_ou_reservados).order_by('nome')


class ReservaCreateView(LoginRequiredMixin, generic.CreateView):
    model = Movimentacao
    
    fields = ['reservaInicio', 'reservaFim']
    
    template_name = 'ces/reserva.html'

    def dispatch(self, *args, **kwargs):       
        self.objeto_id =  kwargs['pk']
        
        return super(ReservaCreateView, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(ReservaCreateView, self).get_context_data(**kwargs)
        objeto = get_object_or_404(Objeto, pk=self.objeto_id)
        context['objeto'] = objeto

        return context

    def form_valid(self, form):
        objeto = Objeto.objects.get(id=self.objeto_id)
        form.instance.objeto=objeto
        form.instance.usuario=self.request.user
        form.instance.status = 8
        form.save()
        objeto.status = 3
        objeto.save()
        
        return HttpResponse(render_to_string('ces/reserva.html', {'objeto': objeto}))
        