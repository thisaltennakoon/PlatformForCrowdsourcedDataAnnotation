# Generated by Django 3.0.5 on 2020-05-26 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataAnnotationResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TaskID', models.CharField(max_length=30)),
                ('DataInstance', models.CharField(max_length=30)),
                ('ClassID', models.IntegerField(default=0)),
                ('UserID', models.IntegerField()),
                ('LastUpdate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DataGenerationResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TaskID', models.CharField(max_length=30)),
                ('DataInstance', models.CharField(max_length=30)),
                ('GenerationResult', models.CharField(max_length=400)),
                ('UserID', models.IntegerField()),
                ('LastUpdate', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
