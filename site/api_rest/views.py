from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from api_rest import serializers
from ces import models
from datetime import datetime


class ObjetosServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        objetos =  models.Objeto.objects.filter()
        serializer = serializers.ObjetoSerializer(objetos, many=True)
        return Response(serializer.data)


class ObjetoServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, objeto_id, format=None):
        objeto =  models.Objeto.objects.get(id=objeto_id)
        serializer = serializers.ObjetoSerializer(objeto)
        return Response(serializer.data)


class ObjetoDisponivelServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        objetos =  models.Objeto.objects.all()
        movimentacoes = models.Movimentacao.objects.filter(devolucao=None)
        movimentacoes_objetos = []
        objetos_list = []
        for mov in movimentacoes:
            movimentacoes_objetos.append(mov.objeto_id)
        for obj in objetos:
            if obj not in movimentacoes_objetos:
                objetos_list.append(obj)
        serializer = serializers.ObjetoSerializer(objetos_list, many=True)
        return Response(serializer.data)


class ObjetoDisponivelUsuarioServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id, format=None):
        objetos =  models.Objeto.objects.all()
        movimentacoes = models.Movimentacao.objects.filter(devolucao=None)
        movimentacoes_objetos = []
        objetos_list = []
        for mov in movimentacoes:
            movimentacoes_objetos.append(mov.objeto_id)
        for obj in objetos:
            if obj not in movimentacoes_objetos:
                # IF --> Verificar se o usuário tem permissão para exibir tal objeto
                objetos_list.append(obj)
        serializer = serializers.ObjetoSerializer(objetos_list, many=True)
        return Response(serializer.data)


class MovimentacaoUsuarioServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id, format=None):
        user = models.Usuario.objects.get(id=user_id)
        movimentacoes =  models.Movimentacao.objects.filter(usuario_id__id=user.id)
        serializer = serializers.MovimentacaoSerializer(movimentacoes, many=True)
        return Response(serializer.data)


class DetalheMovimentacaoServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, movimentacao_id, format=None):
        movimentacao =  models.Movimentacao.objects.get(id=movimentacao_id)
        serializer = serializers.MovimentacaoSerializer(movimentacao)
        return Response(serializer.data)


class MovimentacaoAbertaUsuarioServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id, format=None):
        user = models.Usuario.objects.get(id=user_id)
        movimentacoes =  models.Movimentacao.objects.filter(usuario_id__id=user.id, devolucao=None)
        serializer = serializers.MovimentacaoSerializer(movimentacoes, many=True)
        return Response(serializer.data)


class EmprestarObjetoServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        # PRECISA VERIFICAR SE O NOVO USUÁRIO TEM
        # PERMISSÃO PARA PEGA O OBJETO ANTES DE TUDO
        objeto_id = request.data.get('objeto_id')
        objeto = models.Objeto.objects.get(id=objeto_id)
        usuario_id = request.data.get('usuario_id')
        usuario = models.Usuario.objects.get(id=usuario_id)

        movimentacao = models.Movimentacao.objects.create(retirada = datetime.now(),devolucao=None,
                                                              objeto_id=objeto, usuario_id=usuario)
        return Response(200)


class DevolverObjetoServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        movimentacao_id =  request.data.get('movimentacao_id')

        movimentacao = models.Movimentacao.objects.get(id=movimentacao_id)
        movimentacao.devolucao = datetime.now()
        movimentacao.save()

        serializer = serializers.MovimentacaoSerializer(movimentacao)
        return Response(serializer.data)


class TransferirObjetoServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        # PRECISA VERIFICAR SE O NOVO USUÁRIO TEM
        # PERMISSÃO PARA PEGAR O OBJETO ANTES DE TUDO
        objeto_id = request.data.get('objeto_id')
        objeto = models.Objeto.objects.get(id=objeto_id)
        usuario_id = request.data.get('usuario_id')
        usuario = models.Usuario.objects.get(id=usuario_id)
        novo_usuario_id = request.data.get('novo_usuario_id')
        novo_usuario = models.Usuario.objects.get(id=novo_usuario_id)

        movimentacao_id =  request.data.get('movimentacao_id')
        movimentacao = models.Movimentacao.objects.get(id=movimentacao_id)
        movimentacao.devolucao = datetime.now()
        movimentacao.save()

        movimentacao = models.Movimentacao.objects.create(retirada = datetime.now(),devolucao=None,
                                                              objeto_id=objeto, usuario_id=novo_usuario)
        return Response(200)
