# Generated by Django 2.2.1 on 2019-05-09 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='feature_abs',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='feature_is_R',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='feature_name',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='feature_path',
        ),
    ]
