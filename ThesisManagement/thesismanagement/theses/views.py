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
            return Response({"message": "Khóa luận chỉ được thực hiện    bởi 1 đển 2 sinh viên"}, status=status.HTTP_400_BAD_REQUEST)

        lecturer_count = len(data.get('lecturers'))
        if lecturer_count < configs.MIN_LECTURER or lecturer_count > configs.MAX_LECTURER:
            return Response({"message": "Khóa luận chỉ được hướng dẫn bởi 1 đển 2 giảng viên"}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    @action(methods=['post'], url_path='scores', detail=True)
    def add_score(self, request, pk):
        user = request.user
        member = Member.objects.get(lecturer_id=user.id, committee_id=self.get_object().committee_id)
        s = Score.objects.create(thesis=self.get_object(), member=member, criteria_id=request.data.get('criteria_id'), score=request.data.get('score'))
        s.save()

        return Response(serializers.ThesisDetailSerializer(s.thesis).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='committee', detail=True)
    def add_committee(self, request, pk):
        committee_id = request.data.get('committee_id')

        committee = Committee.objects.get(id=committee_id)
        if committee.theses.count() >= configs.MAX_THESIS:
            return Response({"message": "Hội đồng đã chấm tối đa 5 khóa luận"}, status=status.HTTP_400_BAD_REQUEST)

        thesis = self.get_object()
        thesis.committee_id = committee_id
        thesis.save()

        return Response(serializers.ThesisDetailSerializer(thesis).data, status.HTTP_200_OK)


class CommitteeViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Committee.objects.all()
    serializer_class = serializers.CommitteeSerializer
    permission_classes = [perms.IsAcademicManagerAuthenticated()]

    def get_permissions(self):
        if self.action in ['retrieve', 'get_theses']:
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
            return Response({"message": "Hội đồng chỉ được từ 3 đến 5 thành viên"}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)

    @action(methods=['get'], url_path='theses', detail=True)
    def get_theses(self, request, pk):
        theses = self.get_object().theses.filter(active=True)

        return Response(serializers.ThesisDetailSerializer(theses, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


class StudentViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Student.objects.filter(is_active=True).all()
    serializer_class = serializers.StudentDetailSerializer
    permission_classes = [perms.IsAcademicManagerAuthenticated()]

    def get_permissions(self):

        if self.action in ['retrieve']:
            return [permissions.OR(perms.IsStudentOfAuthenticated(), perms.IsAcademicManagerAuthenticated())]

        return self.permission_classes


class LecturerViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Lecturer.objects.filter(is_active=True).all()
    serializer_class = serializers.LecturerDetailSerializer
    permission_classes = [perms.IsAcademicManagerAuthenticated()]

    def get_permissions(self):
        if self.action in ['retrieve']:
            return [permissions.OR(perms.IsLecturerOfAuthenticated(), perms.IsAcademicManagerAuthenticated())]

        return self.permission_classes


class CriteriaViewSet(viewsets.ViewSet,generics.CreateAPIView, generics.ListAPIView):
    queryset = Criteria.objects.filter(active=True).all()
    serializer_class = serializers.CriteriaDetailSerializer
    permission_classes = [perms.IsAcademicManagerAuthenticated()]

    def get_permissions(self):
        if self.action in ['list']:
            return [permissions.OR(perms.IsAcademicManagerAuthenticated(), perms.IsLecturerOfAuthenticated())]

        return self.permission_classes


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializers.UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], url_path='current-user', url_name='current-user', detail=False)
    def current_user(self, request):
        return Response(serializers.UserDetailSerializer(request.user).data)

    @action(methods=['patch'], url_path='change-password', detail=False)
    def change_password(self, request):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password and confirm_password and password == confirm_password:
            user = request.user
            user.set_password(request.data.get('password'))
            user.save()

            return Response(serializers.UserDetailSerializer(user).data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)