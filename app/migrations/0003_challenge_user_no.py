# Generated by Django 4.2.5 on 2023-09-23 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_challengedetail_reg_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='user_no',
            field=models.IntegerField(default=0),
        ),
    ]
