# Generated by Django 4.2.1 on 2023-05-10 18:47

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0003_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="content",
            field=tinymce.models.HTMLField(default=None),
        ),
    ]