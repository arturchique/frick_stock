from django.contrib.auth.models import AnonymousUser
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


class UserView(APIView):
    """ Методы для получения информации о пользователе """
    def get(self, request):

