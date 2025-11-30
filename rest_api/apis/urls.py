from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apis.views.v1 import school, classroom, teacher, student

router = DefaultRouter()

# api_v1_urls = (router.urls, 'v1')
router.register(r'schools', school.SchoolViewSet, basename='school')
router.register(r'classrooms', classroom.ClassroomViewSet, basename='classroom')
router.register(r'teachers', teacher.TeacherViewSet, basename='teacher')
router.register(r'students', student.StudentViewSet, basename='student')

urlpatterns = [
    path('v1/', include(router.urls))
]

