# Generated by Django 4.2 on 2025-02-27 15:56

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("image", models.ImageField(upload_to="")),
            ],
        ),
        migrations.CreateModel(
            name="Video",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("video", models.FileField(upload_to="")),
            ],
        ),
    ]
