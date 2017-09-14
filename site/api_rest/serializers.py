from rest_framework import serializers
from ces import models


class MovimentacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Movimentacao
        fields = ('id', 'retirada', 'devolucao', 'objeto_id', 'usuario_id')
        depth = 1


class ObjetoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Objeto
        fields = ('id', 'nome', 'tipoObjeto_id')
        depth = 1
