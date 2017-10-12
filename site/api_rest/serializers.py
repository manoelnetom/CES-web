from rest_framework import serializers
from ces import models


class ObjetoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Objeto
        fields = ('id', 'nome', 'tipoObjeto_id', 'status')
        depth = 1


class MovimentacaoSerializer(serializers.ModelSerializer):

    objeto_id = ObjetoSerializer()
    class Meta:
        model = models.Movimentacao
        fields = ('id', 'retirada', 'devolucao', 'objeto_id', 'usuario_id', 'status')
        depth = 1


class PerfilUsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PerfilUsuario
        fields = ('id', 'nome')
        depth = 1

class UsuarioSerializer(serializers.ModelSerializer):

    profileName = PerfilUsuarioSerializer()
    class Meta:
        model = models.Usuario
        fields = ('id', 'name', 'email', 'profileName')
        depth = 1
