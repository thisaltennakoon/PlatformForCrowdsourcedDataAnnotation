# Generated by Django 3.0.5 on 2020-06-07 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=200)),
                ('Description', models.TextField(blank=True, max_length=255)),
                ('requiredNumofAnnotations', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='GenerationDataSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DataInstance', models.CharField(max_length=255, unique=True)),
                ('NumberOfGenerations', models.IntegerField(default=0)),
                ('TaskID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CreateDataGenerationTask.Task')),
            ],
        ),
    ]
