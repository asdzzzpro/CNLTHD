from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from enum import Enum


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Faculty(BaseModel):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.RESTRICT)


class AcademicManager(User):
    pass


class Lecturer(User):
    theses = models.ManyToManyField('Thesis')


class Major(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Student(User):
    major = models.ForeignKey(Major, on_delete=models.RESTRICT)
    thesis = models.ForeignKey('Thesis', on_delete=models.RESTRICT)


class Committee(BaseModel):
    lecturers = models.ManyToManyField(Lecturer, through='Member')


class LecturerRole(Enum):
    chairman = 1
    secretary = 2
    critical_lecturer = 3
    member = 4


class Member(BaseModel):
    role = models.CharField(LecturerRole, default=LecturerRole.member, max_length=50)
    committee = models.ForeignKey(Committee, on_delete=models.RESTRICT)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.RESTRICT)


class Thesis(BaseModel):
    name = models.CharField(max_length=255, null=False)
    average = models.FloatField(null=True)
    major = models.ForeignKey(Major, on_delete=models.RESTRICT)
    committee = models.ForeignKey(Committee, on_delete=models.RESTRICT)
    criteria = models.ManyToManyField('Criteria', through='Score')


class Criteria(BaseModel):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Score(BaseModel):
    score = models.FloatField(default=0)
    thesis = models.ForeignKey(Thesis, on_delete=models.RESTRICT)
    criteria = models.ForeignKey(Criteria, on_delete=models.RESTRICT)
    lecturer = models.ForeignKey(Member, on_delete=models.RESTRICT)
