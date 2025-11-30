from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from apis.models import School, Classroom, Teacher, Student

class BaseAPITestCase(APITestCase): 
    def setUp(self): 
        self.user = User.objects.create_user(username='testuser', password='1234') 
        self.client.login(username='testuser', password='1234')


class SchoolAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.school1 = School.objects.create(name="School A", short_name="SA")
        self.school2 = School.objects.create(name="School B", short_name="SB")
        self.school_create_url = reverse('school-list')  # URL สำหรับ create & list

    def test_school_list(self):
        response = self.client.get(self.school_create_url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 2)

    def test_school_filter_by_name(self):
        # ทดสอบ filter school ด้วย name
        response = self.client.get(self.school_create_url, {'name': 'School A'},format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'School A')


    def test_school_create(self):
        # ทดสอบ POST สร้าง school
        data = {'name': 'School C', 'short_name': 'SC'}
        response = self.client.post(self.school_create_url, data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 3)

    def test_school_detail(self):
        # ทดสอบ GET detail ของ school
        # สร้าง classroom, teacher, student
        classroom = Classroom.objects.create(school=self.school1, grade='Grade 1', section='A')
        teacher = Teacher.objects.create(first_name='John', last_name='Doe')
        teacher.classrooms.add(classroom)
        student = Student.objects.create(first_name='Alice', last_name='Smith', classroom=classroom)

        url = reverse('school-detail', args=[self.school1.id])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ตรวจสอบ count ของ classroom, teacher, student
        self.assertEqual(response.data['classroom_count'], 1)
        self.assertEqual(response.data['teacher_count'], 1)
        self.assertEqual(response.data['student_count'], 1)

    def test_school_update(self):
        # ทดสอบ PUT อัปเดต school
        url = reverse('school-detail', args=[self.school1.id])
        data = {'name': 'School A Updated', 'short_name': 'SAU'}
        response = self.client.put(url, data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.school1.refresh_from_db()
        self.assertEqual(self.school1.name, 'School A Updated')

    def test_school_delete(self):
        # ทดสอบ DELETE school
        url = reverse('school-detail', args=[self.school2.id])
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(School.objects.filter(id=self.school2.id).exists())


class ClassroomAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.school = School.objects.create(name="School A")
        self.classroom_url = reverse('classroom-list')
        self.classroom = Classroom.objects.create(school=self.school, grade='Grade 1', section='A')

    def test_classroom_list(self):
        # GET list ของ classroom
        response = self.client.get(self.classroom_url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_classroom_filter_by_school(self):
        # Filter classroom ด้วย school
        response = self.client.get(self.classroom_url, {'school': self.school.id},format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        

    def test_classroom_create(self):
        # สร้าง classroom
        data = {'school': self.school.id, 'grade': 'Grade 2', 'section': 'B'}
        response = self.client.post(self.classroom_url, data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Classroom.objects.count(), 2)

    def test_classroom_detail(self):
        # GET classroom detail
        teacher = Teacher.objects.create(first_name='John', last_name='Doe')
        teacher.classrooms.add(self.classroom)
        student = Student.objects.create(first_name='Alice', last_name='Smith', classroom=self.classroom)

        url = reverse('classroom-detail', args=[self.classroom.id])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['teachers']), 1)
        self.assertEqual(len(response.data['students']), 1)


    def test_classroom_update(self):
        # Update classroom
        url = reverse('classroom-detail', args=[self.classroom.id])
        data = {'school': self.school.id, 'grade': 'Grade 1 Updated', 'section': 'A'}
        response = self.client.put(url, data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.classroom.refresh_from_db()
        self.assertEqual(self.classroom.grade, 'Grade 1 Updated')

    def test_classroom_delete(self):
        # Delete classroom
        url = reverse('classroom-detail', args=[self.classroom.id])
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Classroom.objects.filter(id=self.classroom.id).exists())


class TeacherAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.school = School.objects.create(name="School A")
        self.classroom = Classroom.objects.create(school=self.school, grade='Grade 1', section='A')
        self.teacher_url = reverse('teacher-list')
        self.teacher = Teacher.objects.create(first_name='John', last_name='Doe',gender='M')
        self.teacher.classrooms.add(self.classroom)

    def test_teacher_list(self):
        # GET list ของ teacher
        response = self.client.get(self.teacher_url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_teacher_filter(self):
        # Filter teacher ตาม firstname, lastname, gender, classroom, school
        response = self.client.get(self.teacher_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': 'M',
            'classrooms': self.classroom.id,
            'classrooms__school': self.school.id,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        print(response.data)

    def test_teacher_create(self):
        # สร้าง teacher
        data = {'first_name': 'Alice', 'last_name': 'Smith', 'classrooms': [self.classroom.id]}
        response = self.client.post(self.teacher_url, data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.count(), 2)

    def test_teacher_detail(self):
        # GET teacher detail
        url = reverse('teacher-detail', args=[self.teacher.id])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['classrooms']), 1)

    def test_teacher_update(self):
        # Update teacher
        url = reverse('teacher-detail', args=[self.teacher.id])
        data = {'first_name': 'John Updated', 'last_name': 'Doe', 'classrooms': [self.classroom.id]}
        response = self.client.put(url, data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.first_name, 'John Updated')

    def test_teacher_delete(self):
        # Delete teacher
        url = reverse('teacher-detail', args=[self.teacher.id])
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Teacher.objects.filter(id=self.teacher.id).exists())


class StudentAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.school = School.objects.create(name="School A")
        self.classroom = Classroom.objects.create(school=self.school, grade='Grade 1', section='A')
        self.student_url = reverse('student-list')
        self.student = Student.objects.create(first_name='Alice', last_name='Smith', classroom=self.classroom)

    def test_student_list(self):
        # GET list ของ student
        response = self.client.get(self.student_url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_student_filter(self):
        # Filter student ตาม firstname, lastname, gender, classroom, school
        response = self.client.get(self.student_url, {
            'first_name': 'Alice',
            'classroom': self.classroom.id
        },format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_student_create(self):
        # สร้าง student
        data = {'first_name': 'Bob', 'last_name': 'Brown', 'classroom': self.classroom.id}
        response = self.client.post(self.student_url, data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)

    def test_student_detail(self):
        # GET student detail
        url = reverse('student-detail', args=[self.student.id])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['classroom'], self.classroom.id)
        print(response.data)

    def test_student_update(self):
        # Update student
        url = reverse('student-detail', args=[self.student.id])
        data = {'first_name': 'Alice Updated', 'last_name': 'Smith', 'classroom': self.classroom.id}
        response = self.client.put(url, data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, 'Alice Updated')

    def test_student_delete(self):
        # Delete student
        url = reverse('student-detail', args=[self.student.id])
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Student.objects.filter(id=self.student.id).exists())
