from django.shortcuts import render
from django.http import JsonResponse

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.decorators import api_view

@swagger_auto_schema(
    method='GET',
    operation_id='sample api',
    operation_description=
        '테스트용 샘플입니당',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    ),
    tags=['app'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'success': openapi.Schema(type=openapi.TYPE_OBJECT, description="호출하면 성공: 1"),
            }
        )
    )}
)
@api_view(['GET'])
def getSampleApi(request):

    response = {}

    data = {}

    data["success"] = 1

    response["status_code"] = "200"
    response["message"] = "success"
    response["data"] = data

    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
