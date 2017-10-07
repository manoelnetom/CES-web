from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class AbstractModel(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True
        
class TipoObjeto(AbstractModel):
    nome = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Tipo de objeto"
        verbose_name_plural = "Tipos de objeto"


class Objeto(AbstractModel):
    codigo = models.CharField(unique=True, max_length=50, blank=False, null=False)
    nome = models.CharField(unique=True, max_length=50, blank=False, null=False)
    tipoObjeto = models.ForeignKey(TipoObjeto)

    def __str__(self):
        return self.nome

class UsuarioManager(BaseUserManager):
   def create_user(self, matricula, email, nome, sobrenome, password):
        """Creates a new user profile."""

        if not matricula:
            raise ValueError('O campo Matricula é obrigatorio')

        email = self.normalize_email(email)
        user = self.model(matricula=matricula,
                          email=self.normalize_email(email),
                          nome=nome, 
                          password=password)

        user.set_password(password)
        user.save(using=self._db)

        return user

   def create_superuser(self, matricula, email, nome, sobrenome, password):
        """Creates a new user profile."""
       
        user = self.create_user(matricula, email, nome, sobrenome, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
        
class Usuario(AbstractBaseUser, PermissionsMixin):
    matricula = models.CharField(max_length=16, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=30)
    telefone = models.CharField(max_length=250, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
        
    date_joined = models.DateTimeField(auto_now_add = True)

    objects = UsuarioManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'matricula'
    REQUIRED_FIELDS = ['email', 'nome', 'sobrenome']
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"   
      
    def get_full_name(self):
        return '%s %s' % (self.nome, self.sobrenome)

    def get_short_name(self):
        return '%s' % self.nome
   
    def __str__(self):
        return self.get_full_name()
      
class AbstractPerfilModel(Usuario):    
     
    class Meta:
        abstract = True
        
        
class Aluno(AbstractPerfilModel):
    
    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

class Departamento(AbstractModel):
    descricao= models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

class Professor(AbstractPerfilModel):
    departamento = models.ForeignKey(Departamento)
      
    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"


class Setor(AbstractModel):
    descricao = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"

class Funcionario(AbstractPerfilModel):
    setor= models.ForeignKey(Setor)
    class Meta:
        verbose_name = "Funcionario"
        verbose_name_plural = "Funcionarios"
        
  
class Grupo(AbstractModel):
    membros = models.ManyToManyField(settings.AUTH_USER_MODEL, through='GrupoUsuario',  through_fields=('grupo', 'usuario'))
    objetos = models.ManyToManyField(Objeto)
    descricao = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"

        
class GrupoUsuario(AbstractModel):
    usuario =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add = True)
    adicionado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="grupo_adicionado_por")
        
class Movimentacao(AbstractModel):
    retirada = models.DateTimeField(default=timezone.now)
    devolucao = models.DateTimeField(default=timezone.now)
    objeto = models.ForeignKey(Objeto)
    usuario =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"
