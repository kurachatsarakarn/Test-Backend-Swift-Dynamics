from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Classroom(models.Model):
    school = models.ForeignKey(School, related_name='classrooms', on_delete=models.CASCADE)
    grade = models.CharField(max_length=50)  
    section = models.CharField(max_length=50, blank=True)  

    class Meta:
        unique_together = ('school', 'grade', 'section')

    def __str__(self):
        return f"{self.school.short_name or self.school.name} - {self.grade}{('/' + self.section) if self.section else ''}"

class Teacher(models.Model):
    GENDER_CHOICES = (('M','Male'), ('F','Female'), ('O','Other'))

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    classrooms = models.ManyToManyField(Classroom, related_name='teachers', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Student(models.Model):
    GENDER_CHOICES = (('M','Male'), ('F','Female'), ('O','Other'))

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    classroom = models.ForeignKey(Classroom, related_name='students', on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
