# Generated by Django 3.2.23 on 2024-03-18 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Entertainment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Subcategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory', models.TextField()),
                ('description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Entertainment.categories')),
            ],
        ),
        migrations.AlterField(
            model_name='film',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Entertainment.categories'),
        ),
        migrations.AlterField(
            model_name='film',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Entertainment.subcategories'),
        ),
        migrations.AlterField(
            model_name='music',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Entertainment.categories'),
        ),
        migrations.AlterField(
            model_name='music',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Entertainment.subcategories'),
        ),
        migrations.AlterField(
            model_name='video_games',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Entertainment.categories'),
        ),
        migrations.AlterField(
            model_name='video_games',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Entertainment.subcategories'),
        ),
    ]
