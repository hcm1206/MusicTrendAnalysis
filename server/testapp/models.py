from django.db import models

# 고객 모델 정의
class 고객(models.Model):
    고객번호 = models.CharField(max_length=5, primary_key=True)
    고객회사명 = models.CharField(max_length=30)
    담당자명 = models.CharField(max_length=20)
    담당자직위 = models.CharField(max_length=20)
    주소 = models.CharField(max_length=50)
    도시 = models.CharField(max_length=20)
    지역 = models.CharField(max_length=20)
    전화번호 = models.CharField(max_length=20)
    마일리지 = models.IntegerField()

    class Meta:
        db_table = '고객'
        # MySQL 인코딩 설정을 원한다면, settings.py에서 'OPTIONS'를 통해 charset 설정 가능
