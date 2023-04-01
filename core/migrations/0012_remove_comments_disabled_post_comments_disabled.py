# Generated by Django 4.1.7 on 2023-03-31 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_comments_disabled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='disabled',
        ),
        migrations.AddField(
            model_name='post',
            name='comments_disabled',
            field=models.BooleanField(default=False),
        ),
    ]