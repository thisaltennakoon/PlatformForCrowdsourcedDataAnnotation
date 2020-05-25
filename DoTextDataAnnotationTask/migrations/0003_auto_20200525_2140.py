# Generated by Django 3.0.5 on 2020-05-25 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CreateTask', '0004_auto_20200525_2140'),
        ('DoTextDataAnnotationTask', '0002_dataannotationresult_taskid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataannotationresult',
            name='DataInstance',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='dataannotationresult',
            name='TaskID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='textanno', to='CreateTask.Task'),
        ),
    ]