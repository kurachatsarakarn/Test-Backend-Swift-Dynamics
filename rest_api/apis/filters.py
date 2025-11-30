import django_filters
from .models import Teacher, Student, Classroom

# code here



class TeacherFilter(django_filters.FilterSet):
    school = django_filters.NumberFilter(field_name='classrooms__school__id', lookup_expr='exact')
    classroom = django_filters.NumberFilter(field_name='classrooms__id', lookup_expr='exact')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    gender = django_filters.CharFilter(field_name='gender', lookup_expr='exact')

    class Meta:
        model = Teacher
        fields = ['school','classroom','first_name','last_name','gender']

class StudentFilter(django_filters.FilterSet):
    school = django_filters.NumberFilter(field_name='classroom__school__id', lookup_expr='exact')
    classroom = django_filters.NumberFilter(field_name='classroom__id', lookup_expr='exact')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    gender = django_filters.CharFilter(field_name='gender', lookup_expr='exact')

    class Meta:
        model = Student
        fields = ['school','classroom','first_name','last_name','gender']
