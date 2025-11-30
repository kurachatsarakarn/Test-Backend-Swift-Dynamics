from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from ...models import  Classroom

from ...serializers import ClassroomSerializer, ClassroomDetailSerializer



class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.select_related('school').prefetch_related('teachers','students').all().order_by('id')
    serializer_class = ClassroomSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['school']
    search_fields = ['grade','section']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClassroomDetailSerializer
        return ClassroomSerializer
