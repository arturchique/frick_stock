from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.shortcuts import render
from django.core.paginator import Paginator
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
                "data": "Пропущен параметр -- id пользователя (id=...)"
            })
        except ObjectDoesNotExist:
            return Response({
                "status": "error",
                "data": "Пользователя с заданными параметрами не существует"
            })

        serializer = ClientSerializer(client)
        return Response({
            "status": "ok",
            "data": serializer.data
        })


class ClientFilterView(APIView):
    """ Класс, отвечающий за фильтрацию и поиск клиентов """

    def post(self, request):
        """ Возвращает отфильтрованных клиентов или список фильтров с вариантами """
        try:
            search_request = request.data["search"]
            page = request.data["page"] or 1
            filters = request.data["filters"]
        except KeyError:
            return Response({
                "status": "error",
                "data": "Пропущен один или несколько обязательных параметров (search, page, filters)"
            })

        if not filters:
            # Возвращает список фильтров и неотфильтрованные лоты, если фильтры не заданы клиентом
            clients = Client.objects.filter(name__icontains=search_request)
            paginator = Paginator(clients, 15)
            paged_listings = paginator.get_page(page)
            serializer = ClientSerializer(paged_listings, many=True)
            return Response({
                "status": "ok",
                "data": {
                    "filters": {
                        "rating": {
                            "from": 0,
                            "to": 10,
                        },
                        "status": {
                            "b": False,
                            "o": True,
                        },
                    },
                    "clients": serializer.data,
                    "total_page_count": paginator.num_pages
                }
            })
        # Код далее не выполнится, если от клиента поступил запрос с пустыми фильтрами
        status = (key for key, value in filters["status"] if value is True)
        clients = Client.objects.filter(status__in=status,
                                        rating__gte=filters["rating"]["from"],
                                        reting__lte=filters["rating"]["to"],
                                        name__icontains=search_request.lower())
        paginator = Paginator(clients, 15)
        paged_listings = paginator.get_page(page)
        serializer = ClientSerializer(paged_listings, many=True)
        return Response({
            "status": "ok",
            "data": {
                "filters": filters,
                "clients": serializer.data,
                "total_page_count": paginator.num_pages
            }
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
                "data": "Пропущен параметр -- id лота (id=...)"
            })
        except ObjectDoesNotExist:
            return Response({
                "status": "error",
                "data": "Лота с заданными параметрами не существует"
            })

        serializer = LotSerializer(lot)
        return Response({
            "status": "ok",
            "data": serializer.data
        })


class LotFilterView(APIView):
    """ Класс, отвечающий за фильтрацию и поиск лотов """

    def post(self, request):
        """ Возвращает отфильтрованные лоты или список фильтров с вариантами """
        try:
            search_request = request.data["search"]
            page = request.data["page"] or 1
            filters = request.data["filters"]
        except KeyError:
            return Response({
                "status": "error",
                "data": "Пропущен один или несколько обязательных параметров (search, page, filters)"
            })

        if not filters:
            # Возвращает список фильтров и неотфильтрованные лоты, если фильтры не заданы клиентом
            lots = Lot.objects.filter(name__icontains=search_request)
            paginator = Paginator(lots, 15)
            paged_listings = paginator.get_page(page)
            serializer = LotSerializer(paged_listings, many=True)
            return Response({
                "status": "ok",
                "data": {
                    "filters": {
                        "price": {
                            "from": 0,
                            "to": 100000,
                        },
                        "likes": {
                            "from": 0,
                            "to": 10000,
                        },
                    },
                    "lots": serializer.data,
                    "total_page_count": paginator.num_pages
                }
            })
        # Код далее не выполнится, если от клиента поступил запрос с пустыми фильтрами
        lots = Lot.objects.annotate(num_likes=Count('likes')).filter(#price__needed__gte=filters["price"]["from"],
                                                                     num_likes__gte=filters["likes"]["from"],
                                                                     price__needed__lte=filters["price"]["to"],
                                                                     num_likes__lte=filters["likes"]["to"],
                                                                     name__icontains=search_request.lower())
        paginator = Paginator(lots, 15)
        paged_listings = paginator.get_page(page)
        serializer = LotSerializer(paged_listings, many=True)
        return Response({
            "status": "ok",
            "data": {
                "filters": filters,
                "lots": serializer.data,
                "total_page_count": paginator.num_pages
            }
        })
