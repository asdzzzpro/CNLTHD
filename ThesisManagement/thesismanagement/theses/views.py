from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from theses import serializers
from theses.models import *


class ThesisViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Thesis.objects.filter(active=True).all()
    serializer_class = serializers.ThesisSerializer

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


class CommitteeViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Committee.objects.filter(active=True).all()
    serializer_class = serializers.CommitteeSerializer


class StudentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Student.objects.filter(is_active=True).all()
    serializer_class = serializers.StudentDetailSerializer

    @action(methods=['patch'], url_path='change-password', detail=False)
    def change_password(self, request):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password and confirm_password and password == confirm_password:
            user = request.user
            user.set_password(request.data.get('password'))

            return Response(serializers.StudentDetailSerializer(user).data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class LecturerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Lecturer.objects.filter(is_active=True).all()
    serializer_class = serializers.LecturerDetailSerializer

    @action(methods=['patch'], url_path='change-password', detail=False)
    def change_password(self, request):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password and confirm_password and password == confirm_password:
            user = request.user
            user.set_password(request.data.get('password'))
            user.save()

            return Response(serializers.LecturerDetailSerializer(user).data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class CriteriaViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Criteria.objects.filter(active=True).all()
    serializer_class = serializers.CriteriaDetailSerializer
