# Generated by Django 4.1.7 on 2023-03-31 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_post_shared_from'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=500)),
                ('username', models.CharField(max_length=100)),
                ('comment', models.CharField(max_length=500)),
            ],
        ),
    ]