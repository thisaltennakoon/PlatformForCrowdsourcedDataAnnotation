# Generated by Django 3.0.5 on 2020-04-12 03:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('createtask', '0003_auto_20200411_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cateogary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cateogaryName', models.CharField(max_length=250)),
                ('taskID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='createtask.AnnotationTask')),
            ],
        ),
        # migrations.DeleteModel(
        #     name='UserNew1',
        # ),
    ]