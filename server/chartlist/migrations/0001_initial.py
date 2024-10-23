# Generated by Django 5.1.1 on 2024-10-21 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TBL_MA',
            fields=[
                ('Week_Date', models.DateField(primary_key=True, serialize=False)),
                ('Week_Rank', models.IntegerField()),
                ('Title', models.CharField(max_length=128)),
                ('Artist', models.CharField(max_length=128)),
                ('Production', models.CharField(max_length=128)),
                ('Weekly_Views', models.BigIntegerField()),
                ('Genre', models.CharField(max_length=32)),
                ('Runtime', models.CharField(max_length=32)),
                ('New_Artist', models.CharField(max_length=128)),
                ('n_score', models.FloatField()),
                ('g_score', models.FloatField()),
                ('Rank_lag_1', models.IntegerField()),
                ('Rank_lag_2', models.IntegerField()),
                ('Rank_lag_3', models.IntegerField()),
            ],
            options={
                'db_table': 'TBL_MA',
            },
        ),
    ]