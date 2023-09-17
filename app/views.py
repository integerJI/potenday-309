from django.shortcuts import render
from django.http import JsonResponse

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response

from .models import Challenge
from .serializers import ChallengeSerializer, ChallengeDetailSerializer, ImageSerializer

@api_view(['GET'])
def getSampleApi(request):
    data = {
        'status_code': 200,
        'message': 'success',
        'data': {
            'success': 1
        }
    }
    return Response(data)

class ChallengeListCreateView(generics.ListCreateAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status_code': 200,
            'message': 'success',
            'data': serializer.data
        })

class ChallengeRetrieveView(generics.RetrieveAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status_code': 200,
            'message': 'success',
            'data': serializer.data
        })
