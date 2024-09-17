# Generated by Django 5.1.1 on 2024-09-17 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Дата создания"),
        ),
        migrations.AlterField(
            model_name="product",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
        ),
    ]
