from django.contrib import admin

# Register your models here.
from django. contrib import admin
from . models import Course, Lesson, Student
admin. site. register(Course)
admin. site. register(Lesson)
admin. site. register(Student)