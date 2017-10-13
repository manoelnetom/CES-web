from django.db import models
from django.utils import timezone
from datetime import datetime
from fontawesome.fields import IconField


STATUS_MOVIMENTACAO = (
    (1, 'Solicitado Retirada'),
    (2, 'Emprestado'),
    (3, 'Solicitado Devolução'),
    (4, 'Devolvido'),
    (5, 'Solicitado Transferência'),
    (6, 'Transferência Pendente'),
    (7, 'Transferência Confirmada'),
    (8, 'Solicitado Reserva')
)

STATUS_OBJETO = (
    (1, 'Disponível'),
    (2, 'Indisponível'),
    (3, 'Pendente'),
)


STATUS_MOVIMENTACOES = {
    (1, 'Solicitado retirada'),
    (2, 'Emprestado'),
    (3, 'Solicitado Devolução'),
    (4, 'Devolvido'),
    (5, 'Solicitado Transferência'),
    (6, 'Transferência confirmada'),
    (7, 'Solicitado Reserva'),
    (8, 'Reserva confirmada'),
}


class TipoObjeto(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome = models.CharField(max_length=50, blank=True, null=True)
    icone = IconField ()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Tipo de objeto"
        verbose_name_plural = "Tipos de objeto"


class Objeto(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome = models.CharField(max_length=50, blank=True, null=True)
    tipoObjeto_id = models.ForeignKey(TipoObjeto)
    status = models.IntegerField(choices=STATUS_OBJETO, default=1)

    def __str__(self):
        return self.nome


class PerfilUsuario(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Perfil de usuário"
        verbose_name_plural = "Perfis de usuário"


class Usuario(models.Model):
    id= models.AutoField(primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=50, unique=True, blank=False,)
    senha = models.TextField(blank=False, null=False)
    profileName = models.ForeignKey(PerfilUsuario)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


class Movimentacao(models.Model):
    id= models.AutoField(primary_key=True, blank=False, null=False)
    retirada = models.DateTimeField(null=True, blank=True)
    devolucao = models.DateTimeField(null=True, blank=True)
    objeto_id = models.ForeignKey(Objeto)
    usuario_id = models.ForeignKey(Usuario)
    status = models.IntegerField(choices=STATUS_MOVIMENTACOES, default=0, blank=True)

    status = models.IntegerField(choices=STATUS_MOVIMENTACAO, default=0)

    def __str__(self):
        return str("{0} para {1}").format(self.objeto_id, self.usuario_id)

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"


class Permissao_Objeto_x_Usuario(models.Model):
    id= models.AutoField(primary_key=True, blank=False, null=False)
    objeto_id = models.ForeignKey(Objeto)
    usuario_id = models.ForeignKey(Usuario)

    def __str__(self):
        return str(self.id)


class Permissao_Objeto_x_PerfilUsuario(models.Model):
    id= models.AutoField(primary_key=True, blank=False, null=False)
    tipoObjeto_id = models.ForeignKey(TipoObjeto)
    perfilUsuario_id = models.ForeignKey(PerfilUsuario)

    def __str__(self):
        return str(self.id)


class Transferencia(models.Model):
    id= models.AutoField(primary_key=True, blank=False, null=False)
    movimentacao_id_origem = models.ForeignKey(Movimentacao, related_name='remetente')
    movimentacao_id_destino = models.ForeignKey(Movimentacao, related_name='destinatario')

    def __str__(self):
        return str("Transferindo {0} de {1} para {2}").format(self.remetente.objeto_id, self.remetente.usuario_id, self.destinatario.usuario_id)

    class Meta:
        verbose_name = "Transferência"
        verbose_name_plural = "Transferências"


class AdminWeb(models.Model):
    id= models.AutoField(primary_key=True, blank=False, null=False)
    tipoObjeto_id = models.ForeignKey(TipoObjeto)
    usuario_id = models.ForeignKey(Usuario)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Admin web"
        verbose_name_plural = "Admins web"
