# Generated by Django 3.0.5 on 2020-05-24 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kurumsal', '0005_auto_20200524_0513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kurumsal',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='kurumsal',
            name='status',
            field=models.CharField(choices=[('True', 'Evet'), ('False', 'Hayir')], max_length=10),
        ),
    ]
