# Generated by Django 3.0.5 on 2020-04-13 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CreateDataAnnotationTask', '0001_initial'),
        ('DoDataAnnotationTask', '0002_auto_20200413_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataannotationresult',
            name='TaskID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CreateDataAnnotationTask.Task'),
        ),
    ]