# Generated by Django 3.0.5 on 2020-06-04 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kurumsal', '0010_auto_20200604_0504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
