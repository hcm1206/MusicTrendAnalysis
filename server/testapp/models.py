from django.db import models

# # 고객 모델 정의
# class 고객(models.Model):
#     고객번호 = models.CharField(max_length=5, primary_key=True)
#     고객회사명 = models.CharField(max_length=30)
#     담당자명 = models.CharField(max_length=20)
#     담당자직위 = models.CharField(max_length=20)
#     주소 = models.CharField(max_length=50)
#     도시 = models.CharField(max_length=20)
#     지역 = models.CharField(max_length=20)
#     전화번호 = models.CharField(max_length=20)
#     마일리지 = models.IntegerField()

#     class Meta:
#         db_table = '고객'
#         # MySQL 인코딩 설정을 원한다면, settings.py에서 'OPTIONS'를 통해 charset 설정 가능


        # TBL_MA 모델 정의
class TBL_MA(models.Model):
    Week_Date = models.DateField(primary_key=True)
    Week_Rank = models.IntegerField()
    Title = models.CharField(max_length=128)
    Artist = models.CharField(max_length=128)
    Production = models.CharField(max_length=128)
    Weekly_Views = models.BigIntegerField()
    Genre = models.CharField(max_length=32)
    Runtime = models.CharField(max_length=32)
    New_Artist = models.CharField(max_length=128)
    n_score = models.FloatField()
    g_score = models.FloatField()
    Rank_lag_1 = models.IntegerField()
    Rank_lag_2 = models.IntegerField()
    Rank_lag_3 = models.IntegerField()

    class Meta:
        db_table = 'TBL_MA'  # MySQL 테이블 이름과 일치시켜야 함
