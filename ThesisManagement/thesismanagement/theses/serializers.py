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
        data = validated_data.copy()

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
    lecturer = LecturerSerializer()

    class Meta:
        model = Member
        fields = ['lecturer', 'role']


class CommitteeSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)

    def create(self, validated_data):
        data = validated_data.copy()

        c = Committee.objects.create(name=data['name'])

        for lecturer in data['members']:
            member = Member.objects.create(committee=c, lecturer_id=lecturer['lecturer']['id'], role=lecturer['role'])
            member.save()

        return c

    class Meta:
        model = Committee
        fields = ['name', 'members']


class CriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = ['id']


class CriteriaDetailSerializer(CriteriaSerializer):
    class Meta:
        model = CriteriaSerializer.Meta.model
        fields = CriteriaSerializer.Meta.fields + ['name']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id']


class ScoreSerializer(serializers.ModelSerializer):
    thesis = ThesisSerializer()
    lecturer = MemberSerializer()

    class Meta:
        model = Score
        fields = ['thesis', 'lecturer', 'criteria_id', 'score']