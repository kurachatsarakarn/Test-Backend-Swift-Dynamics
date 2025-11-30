from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from ...models import School

from ...serializers import SchoolSerializer, SchoolDetailSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all().order_by('id')
    serializer_class = SchoolSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']  
    search_fields = ['name','short_name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SchoolDetailSerializer
        return SchoolSerializer

