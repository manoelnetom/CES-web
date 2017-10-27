from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from api_rest import serializers
from ces import models
from datetime import datetime, timedelta, timezone
import datetime as datetimebase
import pytz


tolerancia = 10; # Tolerância da reserva


class UsuariosServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        usuarios =  models.Usuario.objects.filter()
        serializer = serializers.UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)


class UsuarioServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, usuario_id, format=None):
        usuario =  models.Usuario.objects.get(id=usuario_id)
        serializer = serializers.UsuarioSerializer(usuario)
        return Response(serializer.data)


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
        objetos =  models.Objeto.objects.filter(status=1)
        objetos_list = []

        for obj in objetos:
            tem_reserva = False
            movimentacoes = models.Movimentacao.objects.filter(objeto_id=obj, reserva__isnull=False).all()
            now = datetime.utcnow().replace(tzinfo=pytz.UTC)
            if movimentacoes:
                for mov in movimentacoes:
                    if mov.reserva <= now <= (mov.reserva + timedelta(minutes=tolerancia)):
                        tem_reserva = True
                        break
            if tem_reserva == False:
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
        objeto_id = request.data.get('objeto_id')
        objeto = models.Objeto.objects.get(id=objeto_id)
        tem_reserva = False
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        if objeto.status == 1:
            movimentacoes = models.Movimentacao.objects.filter(objeto_id=objeto, status=8, reserva__isnull=False)
            if movimentacoes:
                for mov in movimentacoes:
                    if mov.reserva < now < (mov.reserva + timedelta(minutes=tolerancia)):
                        tem_reserva = True
                        break
            if tem_reserva == False:
                usuario_id = request.data.get('usuario_id')
                usuario = models.Usuario.objects.get(id = usuario_id)
                models.Movimentacao.objects.create(retirada = now,
                                                   devolucao = None,
                                                   reserva = None,
                                                   objeto_id = objeto,
                                                   usuario_id = usuario,
                                                   status = 1)
                objeto.status = 3
                objeto.save()
                return Response(200)
        return Response(204)


class DevolverObjetoServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        movimentacao_id =  request.data.get('movimentacao_id')

        movimentacao = models.Movimentacao.objects.get(id=movimentacao_id)
        movimentacao.status = 3
        movimentacao.devolucao = datetime.now()
        movimentacao.save()

        return Response(200)


class TransferirObjetoServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        objeto_id = request.data.get('objeto_id')
        objeto = models.Objeto.objects.get(id=objeto_id)
        tem_reserva = False
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        movimentacoes = models.Movimentacao.objects.filter(objeto_id=objeto, status=8, reserva__isnull=False)
        if movimentacoes:
            for mov in movimentacoes:
                if mov.reserva < now < (mov.reserva + timedelta(minutes=tolerancia)):
                    tem_reserva = True
                    break
        if tem_reserva == False:
            movimentacao_id = request.data.get('movimentacao_id')
            movimentacao_origem = models.Movimentacao.objects.get(id=movimentacao_id)
            movimentacao_origem.status = 5
            movimentacao_origem.save()

            novo_usuario_id = request.data.get('novo_usuario_id')
            novo_usuario = models.Usuario.objects.get(id=novo_usuario_id)
            movimentacao_destino = models.Movimentacao.objects.create(retirada = now,
                                               devolucao = None,
                                               reserva = None,
                                               objeto_id = objeto,
                                               usuario_id = novo_usuario,
                                               status = 6)
            tranferencia = models.Transferencia.objects.create(movimentacao_id_origem = movimentacao_origem,
                                                               movimentacao_id_destino = movimentacao_destino)
            return Response(200)
        return Response(204)


class ConfirmarTransferirObjetoServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        movimentacao_origem_id = request.data.get('movimentacao_origem')
        movimentacao_origem = models.Movimentacao.objects.get(id=movimentacao_origem_id)
        movimentacao_origem.status = 7
        movimentacao_origem.devolucao = datetime.now()
        movimentacao_origem.save()

        movimentacao_destino_id = request.data.get('movimentacao_destino')
        movimentacao_destino = models.Movimentacao.objects.get(id=movimentacao_destino_id)
        movimentacao_destino.status = 2
        movimentacao_destino.save()

        return Response(200)


class CancelarTransferirObjetoServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        transferencia_id = request.data.get('transferencia_id')
        transferencia = models.Transferencia.objects.get(id=transferencia_id)

        movimentacao_origem = transferencia.movimentacao_id_origem
        movimentacao_origem.status = 2
        movimentacao_origem.devolucao = None
        movimentacao_origem.save()

        movimentacao_destino = transferencia.movimentacao_id_destino
        movimentacao_destino.delete()

        transferencia.delete()

        return Response(200)


class ListarTransferenciasUsuarioServiceView(APIView):

    def post(self, request, format=None):
        tipo = request.data.get("tipo")
        usuario_id = request.data.get("usuario_id")
        usuario =  models.Usuario.objects.get(id=usuario_id)
        transferencias = None
        if tipo == 1:
            transferencias = models.Transferencia.objects.filter(movimentacao_id_origem__usuario_id=usuario)
        if tipo == 2:
            transferencias = models.Transferencia.objects.filter(movimentacao_id_destino__usuario_id=usuario)
        serializer = serializers.TransferenciaSerializer(transferencias, many=True)
        return Response(serializer.data)


class ExibirTransferenciaServiceView(APIView):

    def post(self, request, format=None):
        transferencia_id = request.data.get("transferencia_id")
        transferencia = models.Transferencia.objects.get(id=transferencia_id)
        serializer = serializers.TransferenciaSerializer(transferencia)
        return Response(serializer.data)


class SolicitarReservaServiceView(APIView):

    def post(self, request, format=None):
        objeto_id = request.data.get('objeto_id')
        objeto = models.Objeto.objects.get(id=objeto_id)
        tem_reserva = False
        data_reserva_str = request.data.get('data_reserva')
        data_reserva_obj = datetime.strptime(data_reserva_str, '%d/%m/%Y %H:%M').replace(tzinfo=pytz.UTC)
        if objeto.status == 1:
            movimentacoes = models.Movimentacao.objects.filter(objeto_id=objeto, status=8, reserva__isnull=False).all()
            if movimentacoes:
                for mov in movimentacoes:
                    if mov.reserva <= data_reserva_obj <= (mov.reserva + timedelta(minutes=tolerancia)):
                        tem_reserva = True
                        break
            if tem_reserva == False:
                usuario_id = request.data.get('usuario_id')
                usuario = models.Usuario.objects.get(id = usuario_id)
                models.Movimentacao.objects.create(retirada = None,
                                                   devolucao = None,
                                                   reserva = data_reserva_obj,
                                                   objeto_id = objeto,
                                                   usuario_id = usuario,
                                                   status = 8)
                return Response(200)
        return Response(204)


class ExibirReservasAbertasUsuarioServiceView(APIView):

    def post(self, request, format=None):
        usuario_id = request.data.get('usuario_id')
        usuario = models.Usuario.objects.get(id=usuario_id)
        movimentacoes =  models.Movimentacao.objects.filter(usuario_id__id=usuario.id,
                                                            reserva__isnull=False,
                                                            retirada__isnull=True,
                                                            devolucao__isnull=True)
        serializer = serializers.MovimentacaoSerializer(movimentacoes, many=True)
        return Response(serializer.data)


class CancelarReservaServiceView(APIView):

    def post(self, request, format=None):
        movimentacao_id = request.data.get('movimentacao_id')
        movimentacao = models.Movimentacao.objects.filter(id=movimentacao_id).first()
        if movimentacao:
            movimentacao.delete()
            return Response(200)
        return Response(204)


class FiltroMovimentacaoUsuarioServiceView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = models.Usuario.objects.get(id=request.data.get('usuario'))
        nome = request.data.get('nome_objeto')
        retirada = request.data.get('data_retirada')
        devolucao = request.data.get('data_devolucao')
        status = request.data.get('status')
        tipo = request.data.get('tipo_objeto')

        movimentacoes =  models.Movimentacao.objects.filter(usuario_id__id=user.id).all()
        if nome:
            movimentacoes = movimentacoes.filter(objeto_id__nome__contains=nome).all()
        if retirada:
            retirada = datetime.strptime(retirada, '%d/%m/%Y')
            movimentacoes = movimentacoes.filter(retirada__gte=retirada.date()).all()
        if devolucao:
            devolucao = datetime.strptime(devolucao, '%d/%m/%Y')
            movimentacoes = movimentacoes.filter(devolucao__gte=devolucao.date()).all()
        if status:
            movimentacoes = movimentacoes.filter(status=status).all()
        if tipo:
            movimentacoes = movimentacoes.filter(objeto_id__tipoObjeto_id=tipo).all()

        serializer = serializers.MovimentacaoSerializer(movimentacoes, many=True)
        return Response(serializer.data)


class ObjectStatusListServiceView(APIView):

    def get(self, request, format=None):
        status = models.STATUS_OBJETO
        status_list = [dict(valor=s[0], descricao=s[1]) for s in status]
        return Response(status_list, 200)
