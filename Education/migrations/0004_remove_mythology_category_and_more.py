# Generated by Django 4.2.3 on 2024-03-28 13:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Education", "0003_history_mythology_science_and_nature"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mythology",
            name="category",
        ),
        migrations.RemoveField(
            model_name="mythology",
            name="subcategory",
        ),
        migrations.RemoveField(
            model_name="science_and_nature",
            name="category",
        ),
        migrations.RemoveField(
            model_name="science_and_nature",
            name="subcategory",
        ),
        migrations.RemoveField(
            model_name="subcategories",
            name="category",
        ),
        migrations.DeleteModel(
            name="History",
        ),
        migrations.DeleteModel(
            name="Mythology",
        ),
        migrations.DeleteModel(
            name="Science_and_Nature",
        ),
        migrations.DeleteModel(
            name="Subcategories",
        ),
    ]
