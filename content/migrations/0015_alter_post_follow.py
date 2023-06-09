# Generated by Django 4.2.1 on 2023-05-17 18:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("content", "0014_post_like"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="follow",
            field=models.ManyToManyField(
                related_name="postsfollow",
                through="content.PostUserFavourite",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
