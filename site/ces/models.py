from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission
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

    class Meta:
        verbose_name = "Objeto"
        verbose_name_plural = "Objetos"

    def get_status(self):
       movimentacoes = self.movimentacao_set.filter(retirada_isnull=True).order_by('reservaFim');
       if(bool(movimentacoes)):
           return "reservado"
       else:
           movimentacoes = self.movimentacao_set.filter(retirada_isnull=False, devolucao__isnull=True).order_by('reservaFim');
           if(bool(movimentacoes)):
               return "ocupado"
       return "livre"


class GrupoObjeto(models.Model):
    descricao = models.CharField(max_length=50, unique=True, blank=False)
    objetos = models.ManyToManyField(Objeto)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Grupo de Objetos"
        verbose_name_plural = "Grupos de Objetos"


class UsuarioManager(BaseUserManager):
    def create_user(self, matricula, password, **extra_fields):
        """Creates a new user profile."""

        if not matricula:
            raise ValueError('O campo Matricula é obrigatorio')

        user = self.model(matricula = matricula, password = password, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser( self, matricula, password, **extra_fields ):
        """Creates a new user profile."""

        user = self.create_user( matricula, password, **extra_fields )

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    matricula = models.CharField(max_length=16, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    nome = models.CharField(max_length=30, blank=False, null=False)
    sobrenome = models.CharField(max_length=30, blank=False, null=False)
    telefone = models.CharField(max_length=250,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'matricula'

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def get_full_name(self):
        return '%s %s' % (self.nome, self.sobrenome)

    def get_short_name(self):
        return '%s' % self.nome

    def __str__(self):
        return self.get_full_name()


class Aluno(Usuario):

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    def save(self, *args, **kwargs):
        super(Aluno, self).save(*args, **kwargs)

        permissions = Permission.objects.filter(content_type__model='movimentacao'
                      ).exclude(codename__contains='delete'
                      ).exclude(codename__contains='see_details'
                      ).exclude(codename__contains='back_objeto')

        self.user_permissions.set(permissions)

        super(Aluno, self).save(*args, **kwargs)


class Departamento(AbstractModel):
    descricao = models.CharField(max_length=50, unique=True, blank=False)

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

    def save(self, *args, **kwargs):
        super(Professor, self).save(*args, **kwargs)

        permissions = Permission.objects.filter(content_type__model='movimentacao'
                      ).exclude(codename__contains='delete'
                      ).exclude(codename__contains='back_objeto')

        self.user_permissions.set(permissions)

        super(Professor, self).save(*args, **kwargs)


class Setor(AbstractModel):
    descricao = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"


class Funcionario(Usuario):
    setor = models.ForeignKey(Setor)

    class Meta:
        verbose_name = "Funcionario"
        verbose_name_plural = "Funcionarios"

    def save(self, *args, **kwargs):
        self.is_staff = True
        super(Funcionario, self).save(*args, **kwargs)

        permissions = Permission.objects.filter(content_type__app_label='ces'
                      ).exclude(content_type__model='movimentacao',
                      codename__contains='delete')

        self.user_permissions.set(permissions)

        super(Funcionario, self).save(*args, **kwargs)


class GrupoUsuario(AbstractModel):
    descricao = models.CharField(max_length=50, unique=True, blank=False)
    usuarios = models.ManyToManyField(settings.AUTH_USER_MODEL)
    acessos = models.ManyToManyField(GrupoObjeto)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Grupo de usuários"
        verbose_name_plural = "Grupos de usuários"


class Movimentacao(AbstractModel):
    reservaInicio = models.DateTimeField(default=timezone.now)
    reservaFim = models.DateTimeField(default=timezone.now)
    retirada = models.DateTimeField(null=True)
    devolucao = models.DateTimeField(null=True)
    objeto = models.ForeignKey(Objeto)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"
        permissions = (
            ("can_see_details_movement", "Can see details Movimentacao"),
            ("can_mark_returned", "Set Objeto as returned")
        )
