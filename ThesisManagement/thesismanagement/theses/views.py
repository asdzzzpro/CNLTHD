from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from theses import serializers, perms, configs
from theses.models import *


class ThesisViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Thesis.objects.all()
    serializer_class = serializers.ThesisSerializer
    permission_classes = [perms.IsAcademicManagerAuthenticated()]

    def get_permissions(self):
        if self.action in ['list']:
            return [permissions.OR(perms.IsAcademicManagerAuthenticated(), perms.IsLecturerAuthenticated())]

        if self.action in ['retrieve']:
            return [permissions.OR(permissions.OR(perms.IsAcademicManagerAuthenticated(), perms.IsStudentThesisOfAuthenticated()), perms.IsLecturerAuthenticated())]

        if self.action in ['add_score']:
            return [perms.IsMemberOfThesisAuthenticated()]

        return self.permission_classes

    def list(self, request, *args, **kwargs):
        return Response(serializers.ThesisDetailSerializer(self.get_queryset(), many=True).data)

    def retrieve(self, request, *args, **kwargs):
        return Response(serializers.ThesisDetailSerializer(self.get_object()).data)

    def create(self, request, *args, **kwargs):
        data = request.data

        student_count = len(data.get('students'))
        if student_count < configs.MIN_STUDENT or student_count > configs.MAX_STUDENT:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        lecturer_count = len(data.get('lecturers'))
        if lecturer_count < configs.MIN_LECTURER or lecturer_count > configs.MAX_LECTURER:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    @action(methods=['post'], url_path='scores', detail=True)
    def add_score(self, request, pk):
        user = request.user
        member = Member.objects.get(lecturer_id=user.id, committee_id=self.get_object().committee_id)
        s = Score.objects.create(thesis=self.get_object(), member=member, criteria_id=request.data.get('criteria_id'), score=request.data.get('score'))
        s.save()

        return Response(serializers.ScoreSerializer(s).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='committee', detail=True)
    def add_committee(self, request, pk):
        thesis = self.get_object()
        thesis.committee_id = request.data.get('committee_id')
        thesis.save()

        return Response(serializers.ThesisDetailSerializer(thesis).data, status.HTTP_200_OK)


class CommitteeViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Committee.objects.all()
    serializer_class = serializers.CommitteeSerializer
    permission_classes = [perms.IsAcademicManagerAuthenticated()]

    def get_permissions(self):
        if self.action in ['retrieve']:
            return [permissions.OR(perms.IsAcademicManagerAuthenticated(), perms.IsMemberOfCommitteeOfAuthenticated())]

        return self.permission_classes

    def retrieve(self, request, *args, **kwargs):
        return Response(serializers.CommitteeDetailSerializer(self.get_object()).data)

    def list(self, request, *args, **kwargs):
        return Response(serializers.CommitteeDetailSerializer(self.get_queryset(), many=True).data)
    
    def create(self, request, *args, **kwargs):
        data = request.data

        member_count = len(data.get('members'))
        if member_count < configs.MIN_MEMBER or member_count > configs.MAX_MEMBER:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)


class StudentViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Student.objects.filter(is_active=True).all()
    serializer_class = serializers.StudentDetailSerializer
    permission_classes = [perms.IsAcademicManagerAuthenticated()]

    def get_permissions(self):
        if self.action in ['change_password']:
            return [perms.IsStudentOfAuthenticated()]

        if self.action in ['retrieve']:
            return [permissions.OR(perms.IsStudentOfAuthenticated(), perms.IsAcademicManagerAuthenticated())]

        return self.permission_classes

    @action(methods=['patch'], url_path='change-password', detail=False)
    def change_password(self, request):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password and confirm_password and password == confirm_password:
            user = request.user
            user.set_password(request.data.get('password'))
            user.save()

            return Response(serializers.StudentDetailSerializer(user.student).data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class LecturerViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Lecturer.objects.filter(is_active=True).all()
    serializer_class = serializers.LecturerDetailSerializer
    permission_classes = [perms.IsAcademicManagerAuthenticated()]

    def get_permissions(self):
        if self.action in ['change_password']:
            return [perms.IsLecturerOfAuthenticated()]

        if self.action in ['retrieve']:
            return [permissions.OR(perms.IsLecturerOfAuthenticated(), perms.IsAcademicManagerAuthenticated())]

        return self.permission_classes

    @action(methods=['patch'], url_path='change-password', detail=False)
    def change_password(self, request):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password and confirm_password and password == confirm_password:
            user = request.user
            user.set_password(request.data.get('password'))
            user.save()

            return Response(serializers.LecturerDetailSerializer(user.lecturer).data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class CriteriaViewSet(viewsets.ViewSet,generics.CreateAPIView, generics.ListAPIView):
    queryset = Criteria.objects.filter(active=True).all()
    serializer_class = serializers.CriteriaDetailSerializer
    permission_classes = [perms.IsAcademicManagerAuthenticated()]

    def get_permissions(self):
        if self.action in ['list']:
            return [permissions.OR(perms.IsAcademicManagerAuthenticated(), perms.IsLecturerOfAuthenticated())]

        return self.permission_classes
