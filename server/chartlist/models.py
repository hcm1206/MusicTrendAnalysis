from django.db import models

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