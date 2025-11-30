from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from ...models import  Student

from ...serializers import StudentSerializer, StudentDetailSerializer

from ...filters import  StudentFilter


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('classroom','classroom__school').all().order_by('id')
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = StudentFilter
    search_fields = ['first_name','last_name']
    ordering_fields = ['first_name','last_name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StudentDetailSerializer
        return StudentSerializer
