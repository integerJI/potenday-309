from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import date, timedelta
from django.views import View
from django.http import HttpResponseRedirect

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Challenge, ChallengeDetail, Image
from .serializers import ChallengeSerializer, ChallengeDetailSerializer, ImageSerializer
from pathlib import Path
import os, json, requests
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

secret_file = os.path.join(BASE_DIR, 'secrets.json')

def index(request):
    render (request, 'index.html')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

class KakaoSignInView(View):
    def get(self, request):
        cliend_id = get_secret("SOCIAL_AUTH_KAKAO_KEY")
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={cliend_id}&redirect_uri=http://13.209.70.9/oauth/kakao/login/callback/token/&response_type=code"
        )
    
class KakaoSignInViewToken(View):
    def get(self, request):
        code = request.GET.get('code')
        cliend_id = get_secret("SOCIAL_AUTH_KAKAO_KEY")
        client_secret = get_secret("SOCIAL_AUTH_KAKAO_SECRET")

        # Kakao OAuth 서버에 토큰을 요청할 데이터 설정
        data = {
            'grant_type': 'authorization_code',
            'client_id': cliend_id,  # Kakao 애플리케이션의 클라이언트 ID로 변경
            'client_secret' : client_secret,
            'redirect_uri': 'http://13.209.70.9/oauth/kakao/login/callback/token/',
            'code': code,
        }

        # Kakao OAuth 서버로 POST 요청을 보냅니다.
        response = requests.post('https://kauth.kakao.com/oauth/token', data=data)

        # 응답 확인
        if response.status_code == 200:
            # 토큰 발급 성공 시 응답을 JSON 형식으로 반환
            token_data = response.json()

            # Authorization 헤더에 토큰 추가
            authorization_header = f"Bearer {token_data['access_token']}"

            # 리다이렉션 URL 생성
            redirection_url = 'https://one-hundred-me.github.io/web/'
            
            # 리다이렉션 시 Authorization 헤더를 포함하여 보냅니다.
            return HttpResponseRedirect(redirection_url, headers={'Authorization': authorization_header})

        else:
            # 토큰 발급 실패 시 에러 응답을 반환
            error_data = {'error': 'Failed to obtain access token'}
            return JsonResponse(error_data, status=400)

class KakaoUserInfoView(View):
    def get(self, request):
        # 액세스 토큰을 요청에서 가져오거나 세션에서 추출합니다.
        access_token = request.GET.get('access_token')

        # 액세스 토큰이 없으면 오류 응답 반환
        if not access_token:
            return JsonResponse({'error': 'Access token is missing'}, status=400)

        # Kakao API 서버에 사용자 정보 요청
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            # 여기에서 user_data를 원하는 방식으로 처리합니다.
            # 예를 들어, user_data에서 사용자의 고유 ID나 닉네임을 추출할 수 있습니다.
            user_id = user_data['id']

            # 사용자 정보를 JSON 응답으로 반환
            return JsonResponse({'user_id': user_id})
        else:
            # Kakao API 서버에서 오류 응답이 온 경우
            error_data = response.json()
            return JsonResponse(error_data, status=response.status_code)

class UserChallengesListView(APIView):
    def extract_user_id(self, access_token):
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data['id']
            return user_id
        else:
            return 0

    def get(self, request):
        access_token = request.META.get('HTTP_AUTHORIZATION')  # Get the Authorization header value

        # Check if the user is authenticated
        if not access_token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = self.extract_user_id(access_token)

        if user_id is 0:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Find all challenges that match the user_id
        challenges = Challenge.objects.filter(user_no=user_id)

        # Serialize the challenges and return the data
        serializer = ChallengeSerializer(challenges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserChallengesListView(APIView):
    
    def extract_user_id(self, access_token):
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data['id']
            return user_id
        else:
            return 3031272287

    def get(self, request):
        access_token = request.META.get('HTTP_AUTHORIZATION')  # Get the Authorization header value

        # Check if the user is authenticated
        if not access_token:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = self.extract_user_id(access_token)

        if user_id is None:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        # Find all challenges that match the user_id
        challenges = Challenge.objects.filter(user_no=user_id)

        # Serialize the challenges
        serializer = ChallengeSerializer(challenges, many=True)
        
        # Create a custom response
        response_data = {
            'status_code': status.HTTP_200_OK,
            'message': 'Success',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class ChallengeView(APIView):

    def extract_user_id(self, access_token):
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data['id']
            return user_id
        else:
            return 3031272287

    @swagger_auto_schema(
        responses={200: ChallengeSerializer(many=True)},
        operation_description="챌린지 상세",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Access token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get(self, request, pk):
        access_token = request.META.get('HTTP_AUTHORIZATION')  # Get the Authorization header value

        # Check if the user is authenticated
        if not access_token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = self.extract_user_id(access_token)

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
        data['user_info'] = challenge.user_no == user_id

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


class StampList(APIView):

    @swagger_auto_schema(
        responses={200: ChallengeSerializer(many=True)},
        operation_description="챌린지의 스탬프 출력"
    )
    def get(self, request, pk):
        pk = self.kwargs['pk']  # URL에서 pk 값을 가져옵니다.
        challenge = Challenge.objects.get(pk=pk)  # 해당 pk의 Challenge 객체를 가져옵니다.

        # 해당 Challenge 객체의 start_date와 end_date를 얻습니다.
        start_date = challenge.start_date
        end_date = challenge.end_date

        # 날짜 범위 내의 날짜를 생성하고, "0"으로 초기화된 딕셔너리를 생성합니다.
        current_date = start_date
        date_dict = {}

        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            
            # ChallengeDetail에서 데이터를 가져옵니다.
            try:
                challenge_detail = ChallengeDetail.objects.get(challenge_id=pk, reg_date=current_date)
                print(challenge_detail)
                date_dict[date_str] = challenge_detail.success_status
            except ChallengeDetail.DoesNotExist:
                date_dict[date_str] = 0
            
            current_date += timedelta(days=1)

        response_data = {
            'status_code': status.HTTP_200_OK,
            'message': 'Success',
            'data': date_dict
        }
        return Response(response_data)
    

    @swagger_auto_schema(
        responses={200: ChallengeSerializer(many=True)},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'challenge_id': openapi.Schema(type=openapi.TYPE_INTEGER, description= "챌린지 ID"),
                'success_status': openapi.Schema(type=openapi.TYPE_INTEGER, description= "성공 여부 (0: 기본 값, 1: 성공, 2: 실패)"),
            },
        )
    )
    def post(self, request, pk):
        try:
            challenge = Challenge.objects.get(pk=pk)
        except Challenge.DoesNotExist:
            return Response({'message': 'Challenge not found'}, status=status.HTTP_404_NOT_FOUND)

        # 요청에서 'challenge_id'와 'success_status'를 가져옵니다.
        challenge_id = request.data.get('challenge_id')
        success_status = request.data.get('success_status')

        # 필요한 데이터를 기반으로 ChallengeDetail 모델에 데이터를 추가합니다.
        try:
            ChallengeDetail.objects.create(
                challenge_id=challenge_id,
                success_status=success_status,
                # 나머지 필드도 필요한 경우 추가하세요.
            )

            response_data = {
                'status_code': status.HTTP_201_CREATED,
                'message': 'ChallengeDetail created successfully',
                'data': 1  # 수정 성공을 나타내는 데이터
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            error_message = str(e)
            response_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Create failure',
                'data': error_message
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
