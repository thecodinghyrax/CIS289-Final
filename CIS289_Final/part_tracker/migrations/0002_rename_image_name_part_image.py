# Generated by Django 4.2 on 2023-04-21 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('part_tracker', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='part',
            old_name='image_name',
            new_name='image',
        ),
    ]
