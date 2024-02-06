from rest_framework import viewsets, generics
from theses import serializers
from theses.models import *


class ThesisViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Thesis.objects.filter(active=True).all()
    serializer_class = serializers.ThesisSerializer


class CommitteeViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Committee.objects.filter(active=True).all()
    serializer_class = serializers.CommitteeSerializer


class StudentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Student.objects.filter(is_active=True).all()
    serializer_class = serializers.StudentDetailSerializer


class LecturerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Lecturer.objects.filter(is_active=True).all()
    serializer_class = serializers.LecturerDetailSerializer
