# Generated by Django 5.0.3 on 2024-03-11 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_api', '0004_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.TextField(default='Anonymous'),
        ),
    ]
