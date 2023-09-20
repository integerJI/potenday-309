from rest_framework import serializers
from .models import Challenge, ChallengeDetail, Image

# 챌린지 모델 Serializer
class ChallengeSerializer(serializers.ModelSerializer):

    background_image = serializers.IntegerField(
        help_text="배경 이미지 ID"
    )

    blank_image = serializers.IntegerField(
        help_text="빈칸 이미지 ID"
    )

    success_image = serializers.IntegerField(
        help_text="성공 스탬프 이미지 ID"
    )

    failure_image = serializers.IntegerField(
        help_text="실패 스탬프 이미지 ID"
    )

    title = serializers.CharField(
        max_length=200,
        help_text="제목 (최대 200바이트)"
    )

    start_date = serializers.DateField(
        help_text="챌린지 시작일"
    )

    end_date = serializers.DateField(
        help_text="챌린지 종료일"
    )

    count_date = serializers.IntegerField(
        help_text="챌린지 진행 날짜 카운트"
    )

    create_date = serializers.DateTimeField(
        help_text="데이터 생성일"
    )

    class Meta:
        model = Challenge
        fields = '__all__'  # 모든 필드를 포함

# 챌린지 상세 모델 Serializer
class ChallengeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeDetail
        fields = '__all__'  # 모든 필드를 포함

# 이미지 모델 Serializer
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image_type', 'image_url')
        
    # 필드에 대한 설명 추가
    image_type = serializers.IntegerField(
        help_text="이미지 타입, {1: 백그라운드 이미지, 2: 빈배경 이미지, 3: 성공 스탬프 이미지, 4: 실패 스탬프 이미지}"
    )
    image_url = serializers.URLField(
        help_text="이미지 Url"
    )
