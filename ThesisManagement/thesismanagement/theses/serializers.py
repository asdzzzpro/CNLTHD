from .models import *
from rest_framework import serializers


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()
    fullname = serializers.SerializerMethodField(source='fullname')

    def get_fullname(self, user):
        return user.last_name + user.first_name


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ['id', 'name']


class StudentSerializer(UserSerializer):
    class Meta:
        model = Student
        fields = ['id']
        extra_kwargs = {
            'id': {
                'read_only': False
            },
        }


class StudentDetailSerializer(StudentSerializer):
    major = MajorSerializer()

    class Meta:
        model = StudentSerializer.Meta.model
        fields = StudentSerializer.Meta.fields + ['fullname', 'username', 'password', 'email', 'faculty', 'major']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }


class LecturerSerializer(UserSerializer):
    class Meta:
        model = Lecturer
        fields = ['id']
        extra_kwargs = {
            'id': {
                'read_only': False
            },
        }


class LecturerDetailSerializer(LecturerSerializer):
    class Meta:
        model = LecturerSerializer.Meta.model
        fields = LecturerSerializer.Meta.fields + ['fullname', 'username', 'password', 'email', 'faculty']


class ThesisSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)
    lecturers = LecturerSerializer(many=True)

    def create(self, validated_data):
        data = validated_data

        t = Thesis.objects.create(name=data['name'])

        for student in data['students']:
            stu = Student.objects.get(user_ptr_id=student['id'])
            t.students.add(stu)

        for lecturer in data['lecturers']:
            lec = Lecturer.objects.get(user_ptr_id=lecturer['id'])
            t.lecturers.add(lec)

        t.save()

        return t

    class Meta:
        model = Thesis
        fields = ['name', 'students', 'lecturers']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['lecturer', 'role']


class CommitteeSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)

    class Meta:
        model = Committee
        fields = ['name', 'members']