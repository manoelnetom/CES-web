from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from api_rest import serializers
from ces import models
from datetime import datetime


class ObjetoServiceView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        objetos =  models.Objeto.objects.all()
        serializer = serializers.ObjetoSerializer(objetos, many=True)
        return Response(serializer.data)


class ObjetoDisponivelServiceView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id, format=None):
        # Queryset:
        # Verificar se o objeto tem alguma movimentação sem devolucao
        # Verificar se o usuário tem permissão para exibir tal objeto
        return None


class MovimentacaoAbertaServiceView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id, format=None):
        user = models.Usuario.objects.get(id=user_id)
        movimentacoes =  models.Movimentacao.objects.filter(usuario_id__id=user.id, devolucao=None)
        serializer = serializers.MovimentacaoSerializer(movimentacoes, many=True)
        return Response(serializer.data)


class DevolverObjetoServiceView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        movimentacao_id =  request.data.get('movimentacao_id')

        movimentacao = models.Movimentacao.objects.get(id=movimentacao_id)
        movimentacao.devolucao = datetime.now()
        movimentacao.save()

        serializer = serializers.MovimentacaoSerializer(movimentacao)
        return Response(serializer.data)
