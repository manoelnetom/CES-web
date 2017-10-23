from django.shortcuts import render, get_object_or_404

from django.views import generic

from django.http import HttpResponse

from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.template.loader import render_to_string



from .models import Objeto, Movimentacao, GrupoObjeto


class AjaxTemplateMixin(object):

   def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
            if request.is_ajax():
                self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)

@login_required
def index(request):

    pendentes = Movimentacao.objects.filter(usuario__matricula=request.user.matricula, retirada__isnull=False, devolucao__isnull=True)

    reservados = Movimentacao.objects.filter(usuario__matricula=request.user.matricula, retirada__isnull=True)

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

      return Objeto.objects.filter(grupoobjeto__in=GrupoObjeto.objects.filter(grupousuario__usuarios__matricula=self.request.user.matricula))


class FazerReservaView(SuccessMessageMixin, AjaxTemplateMixin, generic.CreateView):
    model = Movimentacao

    fields = ['reservaInicio', 'reservaFim']

    success_url = reverse_lazy('reserva')
    success_message = "Way to go!"

    template_name = 'ces/fazer_reserva_inner.html'

    def dispatch(self, *args, **kwargs):
        self.objeto_id =  kwargs['pk']

        return super(FazerReservaView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FazerReservaView, self).get_context_data(**kwargs)
        objeto = get_object_or_404(Objeto, pk=self.objeto_id)
        context['objeto'] = objeto

        return context

    def form_valid(self, form):
        objeto = Objeto.objects.get(id=self.objeto_id)
        form.instance.objeto=objeto
        form.instance.usuario=self.request.user
        form.save()

        return HttpResponse(render_to_string('ces/reserva_modal_sucess.html', {'objeto': objeto}))
