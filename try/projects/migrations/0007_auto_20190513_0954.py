# Generated by Django 2.2.1 on 2019-05-13 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20190513_0942'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mesh',
            old_name='features',
            new_name='feature',
        ),
    ]