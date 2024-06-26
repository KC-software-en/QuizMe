# Generated by Django 4.2.3 on 2024-03-28 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Education", "0004_remove_mythology_category_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subcategories",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subcategory", models.TextField()),
                ("description", models.TextField()),
                (
                    "category",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="Education.categories",
                    ),
                ),
            ],
        ),
    ]
