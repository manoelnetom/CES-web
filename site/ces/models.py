from django.db import models
from django.utils import timezone
from datetime import datetime


class TipoObjeto(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Tipo de objeto"
        verbose_name_plural = "Tipos de objeto"


class Objeto(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    codigo = models.CharField(unique=True, max_length=50, blank=False, null=False)
    nome = models.CharField(unique=True, max_length=50, blank=False, null=False)
    tipoObjeto_id = models.ForeignKey(TipoObjeto)

    def __str__(self):
        return self.nome

class Usuario(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=50, unique=True, blank=False)
    senha = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        
        
class Aluno(Usuario):
    
    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

class Departamento(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    descricao= models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

class Professor(Usuario):
    departamento = models.ForeignKey(Departamento)

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"


class Setor(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    descricao = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"

class Funcionario(Usuario):
    setor= models.ForeignKey(Setor)
    class Meta:
        verbose_name = "Funcionario"
        verbose_name_plural = "Funcionarios"
        
class Permissao(models.Model):
    id  = models.AutoField(primary_key=True, blank=False, null=False)
    descricao = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Permissão"
        verbose_name_plural = "Permissões"       

class Grupo(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    usuarios = models.ManyToManyField(Usuario)
    #permissoes = models.ManyToManyField(Permissao) Verificar qual entidade de permissao irá usar (Permisao ou PermissaoGrupo)
    #permissoes = models.ManyToManyField(PermissaoGrupo)
    descricao = models.CharField(max_length=50, unique=True, blank=False)
    data_criacao = models.DateTimeField(default=timezone.now)
    data_alteracao = models.DateTimeField(default=timezone.now)
    criado_por = models.ForeignKey('auth.User', related_name= 'criado')
    alterado_por = models.ForeignKey('auth.User' , related_name= 'alerado')

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"


class PermissaoGrupo(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    grupo = models.ManyToManyField(Grupo)
    permissao = models.ManyToManyField(Permissao)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "Permissão de Grupo"
        verbose_name_plural = "Permissões de Grupos"

class Movimentacao(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    retirada = models.DateTimeField(default=timezone.now)
    devolucao = models.DateTimeField(default=timezone.now)
    objeto_id = models.ForeignKey(Objeto)
    usuario_id = models.ForeignKey(Usuario)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"
