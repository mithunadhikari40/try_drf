from .serializers import SingerSerializer, SongSerializer, SingerSerializerHyperLinked, SingerSerializerRelated, \
    SongSerializerRelated
from django.shortcuts import render
from rest_framework import viewsets
from .models import Singer, Song


class SingerViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class SingerHyperLinkedViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializerHyperLinked


"""Nested related serializer example"""


class SingerNestedRelatedViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializerRelated


class SongNestedRelatedViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializerRelated
