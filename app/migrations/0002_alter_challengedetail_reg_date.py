# Generated by Django 4.2.5 on 2023-09-21 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengedetail',
            name='reg_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
