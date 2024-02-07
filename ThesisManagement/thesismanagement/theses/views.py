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
        s = Score.objects.create(thesis=self.get_object(), lecturer=request.user, criteria_id=request.data.get('criteria_id'), score=request.data.get('score'))

        return Response(serializers.ScoreSerializer(s).data, status=status.HTTP_201_CREATED)

class CommitteeViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Committee.objects.filter(active=True).all()
    serializer_class = serializers.CommitteeSerializer


class StudentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Student.objects.filter(is_active=True).all()
    serializer_class = serializers.StudentDetailSerializer


class LecturerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Lecturer.objects.filter(is_active=True).all()
    serializer_class = serializers.LecturerDetailSerializer


class CriteriaViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Criteria.objects.filter(active=True).all()
    serializer_class = serializers.CriteriaDetailSerializer