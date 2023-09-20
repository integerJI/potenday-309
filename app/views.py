from django.shortcuts import render
from django.http import JsonResponse

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Challenge, Image
from .serializers import ChallengeSerializer, ChallengeDetailSerializer, ImageSerializer

class ChallengeView(APIView):

    @swagger_auto_schema(
        responses={200: ChallengeSerializer(many=True)},
        operation_description="챌린지 상세"
    )
    def get(self, request, pk):
        try:
            challenge = Challenge.objects.get(pk=pk)
        except Challenge.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ChallengeSerializer(challenge)
        data = serializer.data

        # 이미지 ID를 사용하여 해당 이미지의 URL을 가져와서 추가합니다.
        data['background_image_url'] = get_image_url(data.get('background_image'))
        data['blank_image_url'] = get_image_url(data.get('blank_image'))
        data['success_image_url'] = get_image_url(data.get('success_image'))
        data['failure_image_url'] = get_image_url(data.get('failure_image'))

        response_data = {
            'status_code': status.HTTP_200_OK,
            'message': 'Success',
            'data': data
        }
        return Response(response_data)
    
    @swagger_auto_schema(
        responses={200: ChallengeSerializer(many=True)},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'background_image': openapi.Schema(type=openapi.TYPE_INTEGER),
                'blank_image': openapi.Schema(type=openapi.TYPE_INTEGER),
                'success_image': openapi.Schema(type=openapi.TYPE_INTEGER),
                'failure_image': openapi.Schema(type=openapi.TYPE_INTEGER),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'start_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                'end_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                'count_date': openapi.Schema(type=openapi.TYPE_INTEGER),
                # Add more properties as needed
            },
        )
    )
    def put(self, request, pk):
        try:
            challenge = Challenge.objects.get(pk=pk)
        except Challenge.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ChallengeSerializer(challenge, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status_code': status.HTTP_200_OK,
                'message': 'Update Success',
                'data': 1  # 수정 성공을 나타내는 데이터
            }
            return Response(response_data)
        else:
            error_message = serializer.errors  # 에러 메시지 추출
            response_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Update failure',
                'data': error_message  # 수정 실패 시 에러 메시지를 반환합니다.
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


def get_image_url(image_id):
    try:
        # 이미지 ID를 사용하여 해당 이미지의 URL을 가져옵니다.
        image = Image.objects.get(id=image_id)
        return image.image_url
    except Image.DoesNotExist:
        return None

class ChallengeCreate(generics.CreateAPIView):
    serializer_class = ChallengeSerializer

    @swagger_auto_schema(method='post')  # POST 메소드만 표시
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # 새로운 챌린지 생성
            challenge = serializer.save()
            
            response_data = {
                'status_code': status.HTTP_201_CREATED,
                'message': 'Create Success',
                'data': {
                    'id': challenge.id,
                    # 이미지 관련 필드는 그대로 넣을 것이므로 따로 추가하지 않습니다.
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            error_message = serializer.errors  # 에러 메시지 추출
            response_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Create failure',
                'data': error_message  # 챌린지 생성 실패 시 에러 메시지를 반환합니다.
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
class ImageList(generics.ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')  # URL 패스에서 pk 가져오기
        if pk is not None:
            # pk에 해당하는 이미지만 필터링
            return Image.objects.filter(image_type=pk)
        else:
            return Image.objects.all()  # 모든 이미지 반환
            
    @swagger_auto_schema(
        responses={200: ImageSerializer(many=True)},
        operation_description="Get a list of images with descriptions."
    )
    def list(self, request, *args, **kwargs):
        images = self.get_queryset()
        serializer = self.get_serializer(images, many=True)
        data = serializer.data

        response_data = {
            'status_code': status.HTTP_200_OK,
            'message': 'Success',
            'data': data
        }

        return Response(response_data, status=status.HTTP_200_OK)
