# Generated by Django 4.1.7 on 2023-03-31 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]
