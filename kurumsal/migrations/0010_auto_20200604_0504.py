# Generated by Django 3.0.5 on 2020-06-04 02:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('kurumsal', '0009_auto_20200604_0457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=uuid.uuid1, unique=True),
        ),
    ]
