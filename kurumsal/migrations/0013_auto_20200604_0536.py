# Generated by Django 3.0.5 on 2020-06-04 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kurumsal', '0012_auto_20200604_0535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kurumsal',
            name='slug',
            field=models.SlugField(blank=True, max_length=150),
        ),
    ]