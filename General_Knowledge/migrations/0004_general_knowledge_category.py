# Generated by Django 3.2.23 on 2024-03-21 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('General_Knowledge', '0003_subcategories_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='general_knowledge',
            name='category',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.SET_DEFAULT, to='General_Knowledge.categories'),
        ),
    ]