from rest_framework import serializers
from .models import School, Classroom, Teacher, Student

# code here

class ClassroomSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ('id','grade','section','school')

class TeacherSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id','first_name','last_name','gender')

class StudentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id','first_name','last_name','gender','classroom')


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'short_name', 'address']
    
class SchoolDetailSerializer(SchoolSerializer):
    classroom_count = serializers.SerializerMethodField()
    teacher_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta(SchoolSerializer.Meta):
         fields = SchoolSerializer.Meta.fields + ['classroom_count','teacher_count','student_count']

    def get_classroom_count(self, obj):
        return obj.classrooms.count()

    def get_teacher_count(self, obj):

        return Teacher.objects.filter(classrooms__school=obj).distinct().count()

    def get_student_count(self, obj):
        return Student.objects.filter(classroom__school=obj).count()


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ('id','school','grade','section')

class ClassroomDetailSerializer(ClassroomSerializer):
    teachers = TeacherSimpleSerializer(many=True, read_only=True)
    students = StudentSimpleSerializer(many=True, read_only=True)

    class Meta(ClassroomSerializer.Meta):
        fields = ClassroomSerializer.Meta.fields + ('teachers','students')


class TeacherSerializer(serializers.ModelSerializer):
    classrooms = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all(), many=True, required=False)

    class Meta:
        model = Teacher
        fields = ('id','first_name','last_name','gender','classrooms')

class TeacherDetailSerializer(TeacherSerializer):
    classrooms_detail = ClassroomSimpleSerializer(source='classrooms', many=True, read_only=True)

    class Meta(TeacherSerializer.Meta):
        fields = TeacherSerializer.Meta.fields + ('classrooms_detail',)

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id','first_name','last_name','gender','classroom')

class StudentDetailSerializer(StudentSerializer):
    classroom_detail = ClassroomSimpleSerializer(source='classroom', read_only=True)

    class Meta(StudentSerializer.Meta):
        fields = StudentSerializer.Meta.fields + ('classroom_detail',)
