from django.db import models

class Challenge(models.Model):
    background_image = models.PositiveIntegerField()  # 배경 이미지 ID (정수형)
    blank_image = models.PositiveIntegerField()  # 빈칸 이미지 ID (정수형)
    success_image = models.PositiveIntegerField()  # 성공 이미지 ID (정수형)
    failure_image = models.PositiveIntegerField()  # 실패 이미지 ID (정수형)
    title = models.CharField(max_length=200)  # 제목 (최대 200자 문자열)
    start_date = models.DateField()  # 시작일 (날짜)
    end_date = models.DateField()  # 종료일 (날짜)
    count_date = models.PositiveIntegerField()  # 진행 날짜 카운트
    create_date = models.DateTimeField(auto_now_add=True, null=True)  # 생성일 (자동으로 현재 날짜와 시간 저장)

    def __str__(self):
        return self.title  # 챌린지 모델의 문자열 표현으로 제목을 사용

class ChallengeDetail(models.Model):
    challenge_id = models.PositiveIntegerField()  # 챌린지 ID (정수형)
    image_url = models.URLField()  # 이미지 URL (문자열, URL 형식)
    reg_date = models.DateField(auto_now_add=True, null=True)  # 등록일 (날짜)
    success_status = models.PositiveIntegerField()  # 성공 여부 (정수형)
    memo = models.CharField(max_length=500)  # 메모 (최대 500자 문자열)

    def __str__(self):
        return f"Challenge Detail ID: {self.pk}, Challenge ID: {self.challenge_id}"

class Image(models.Model):
    image_type = models.PositiveIntegerField()  # 이미지 타입 (정수형)
    image_url = models.URLField()  # 이미지 URL (문자열, URL 형식)

    def __str__(self):
        return f"Image ID: {self.pk}, Image Type: {self.image_type}"
