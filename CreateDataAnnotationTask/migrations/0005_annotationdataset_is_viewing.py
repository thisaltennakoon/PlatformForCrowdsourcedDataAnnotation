# Generated by Django 3.0.5 on 2020-04-26 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CreateDataAnnotationTask', '0004_auto_20200425_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotationdataset',
            name='is_viewing',
            field=models.BooleanField(default=False),
        ),
    ]