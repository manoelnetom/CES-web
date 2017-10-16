from django.shortcuts import render
from .models import Objeto,Movimentacao
from django.contrib.auth.decorators import login_required
from django.views import generic

@login_required
def index(request):

    num_objetos = Objeto.objects.all().count();

    return render(
        request,
        'index.html',
        context={'num_objetos': num_objetos},
    )


from django.contrib.auth.mixins import LoginRequiredMixin


class MovimentacaoDeUsuarioListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = Movimentacao
    template_name = 'ces/movimentacao_list_emprestimo_usuario.html'
    paginate_by = 10

    def get_queryset(self):
        return Movimentacao.objects.filter(usuario=self.request.user).order_by('devolucao')