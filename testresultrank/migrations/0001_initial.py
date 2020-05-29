# Generated by Django 3.0.5 on 2020-05-28 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnnotationTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=200)),
                ('Description', models.TextField(blank=True, max_length=256)),
                ('DataInstanceAnnotationTimes', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='User1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=255)),
                ('last_name', models.CharField(default='', max_length=255)),
                ('email', models.EmailField(default='none@email.com', max_length=254)),
                ('country', models.CharField(default='', max_length=255)),
                ('field', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('annotatorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testresultrank.User1')),
                ('testID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testresultrank.AnnotationTest')),
            ],
        ),
        migrations.AddField(
            model_name='annotationtest',
            name='TaskID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testresultrank.Task'),
        ),
    ]