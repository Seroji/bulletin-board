# Generated by Django 4.2.1 on 2023-05-11 16:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0006_comment_like_post_like"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="cover",
            field=models.ImageField(default=None, upload_to="static/news_cover/"),
            preserve_default=False,
        ),
    ]