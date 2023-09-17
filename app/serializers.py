from rest_framework import serializers
from .models import Challenge, ChallengeDetail, Image

# 챌린지 모델 Serializer
class ChallengeSerializer(serializers.ModelSerializer):
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
        fields = '__all__'  # 모든 필드를 포함
