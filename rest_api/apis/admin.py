from django.contrib import admin
from .models import School, Classroom, Teacher, Student
# Register your models here.


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name','short_name')

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('school','grade','section')
    list_filter = ('school',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','gender')
    filter_horizontal = ('classrooms',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','gender','classroom')
    list_filter = ('classroom__school','classroom')
