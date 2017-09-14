from django.db import models
from django.utils import timezone
from datetime import datetime

class TipoObjeto(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome

class Objeto(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome = models.CharField(max_length=50, blank=True, null=True)
    tipoObjeto_id = models.ForeignKey(TipoObjeto)

    def __str__(self):
        return self.nome

class PerfilUsuario(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome

class Usuario(models.Model):
    id= models.AutoField(primary_key=True, blank=False, null=False)
    nome = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=50, unique=True, blank=False,)
    senha = models.TextField(blank=False, null=False)
    perfilUsuario_id = models.ForeignKey(PerfilUsuario)

    def __str__(self):
        return self.nome

class Movimentacao(models.Model):
    id= models.AutoField(primary_key=True, blank=False, null=False)
    retirada = models.DateTimeField(null=True, default=datetime.now)
    devolucao = models.DateTimeField(null=True, default=datetime.now)
    objeto_id = models.ForeignKey(Objeto)
    usuario_id = models.ForeignKey(Usuario)

    def __str__(self):
        return self.id

class Permissao_Objeto_x_Usuario(models.Model):
    id= models.AutoField(primary_key=True, blank=False, null=False)
    objeto_id = models.ForeignKey(Objeto)
    usuario_id = models.ForeignKey(Usuario)

    def __str__(self):
        return self.id

class Permissao_Objeto_x_PerfilUsuario(models.Model):
    id= models.AutoField(primary_key=True, blank=False, null=False)
    tipoObjeto_id = models.ForeignKey(TipoObjeto)
    perfilUsuario_id = models.ForeignKey(PerfilUsuario)

    def __str__(self):
        return self.id

class AdminWeb(models.Model):
    id= models.AutoField(primary_key=True, blank=False, null=False)
    tipoObjeto_id = models.ForeignKey(TipoObjeto)
    usuario_id = models.ForeignKey(Usuario)

    def __str__(self):
        return self.id
