# Generated by Django 3.0.8 on 2020-12-04 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_room_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='max_people',
            field=models.IntegerField(default=5),
        ),
    ]
