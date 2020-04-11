# Generated by Django 3.0.5 on 2020-04-11 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserNew1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='AnnotationTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('decription', models.CharField(max_length=1000)),
                ('status', models.CharField(default='new', max_length=60)),
                ('instructions', models.CharField(max_length=1000)),
                ('creatorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createtask.UserNew1')),
            ],
        ),
    ]
