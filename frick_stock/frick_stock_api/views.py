from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *


class HelloView(APIView):
    def get(self, request):
        return Response({"data": "Hello"})


class FollowsView(APIView):
    """ Методы для работы с подписками и подписчиками """
    def get(self, request):
        """ Возвращает список подписок и подписчиков пользователя """
        user = request.user
        if type(user) == AnonymousUser:
            return Response({
                "status": "error",
                "error": "Невозможно получить информацию о неавторизованном пользователе"
            })

        client = Client.objects.get(user=user)
        follows = client.follows
        followers = client.followers
        follows_serializer = FollowsSerializer(follows, many=True)
        followers_serializer = FollowsSerializer(followers, many=True)

        return Response({
            "status": "ok",
            "data": {
                "follows": follows_serializer.data,
                "followers": followers_serializer.data
            }
        })

    def post(self, request):
        """ Подписывает авторизованного пользователя на заданного """
        pass


class ClientDetailView(APIView):
    """ Методы для работы с информацией о пользователе """
    def get(self, request):
        """ Возвращает информацию о заданном пользователе """
        client_id = request.GET.get("id", "")
        try:
            client = Client.objects.get(id=client_id)
        except ValueError:
            return Response({
                "status": "error",
                "error": "Пропущен параметр -- id пользователя (id=...)"
            })
        except ObjectDoesNotExist:
            return Response({
                "status": "error",
                "error": "Пользователя с заданными параметрами не существует"
            })

        serializer = ClientSerializer(client)
        return Response({
            "status": "ok",
            "data": serializer.data
        })


class LotDetailView(APIView):
    """ Методы для работы с информацией о лотах """
    def get(self, request):
        """ Возвращает информацию о заданном лоте """
        lot_id = request.GET.get("id", "")
        try:
            lot = Lot.objects.get(id=lot_id)
        except ValueError:
            return Response({
                "status": "error",
                "error": "Пропущен параметр -- id лота (id=...)"
            })
        except ObjectDoesNotExist:
            return Response({
                "status": "error",
                "error": "Лота с заданными параметрами не существует"
            })

        serializer = LotSerializer(lot)
        return Response({
            "status": "ok",
            "data": serializer.data
        })