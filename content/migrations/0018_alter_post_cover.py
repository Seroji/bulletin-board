# Generated by Django 4.2.1 on 2023-05-18 19:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0017_alter_post_cover"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="cover",
            field=models.ImageField(upload_to="cover/"),
        ),
    ]
