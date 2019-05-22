# Generated by Django 2.2.1 on 2019-05-13 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_mesh_dir'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statistics',
            old_name='average_area',
            new_name='mean_area',
        ),
        migrations.RemoveField(
            model_name='statistics',
            name='stddev_area',
        ),
        migrations.RemoveField(
            model_name='statistics',
            name='variance_area',
        ),
        migrations.AddField(
            model_name='statistics',
            name='std_area',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='statistics',
            name='var_area',
            field=models.FloatField(default=0),
        ),
    ]