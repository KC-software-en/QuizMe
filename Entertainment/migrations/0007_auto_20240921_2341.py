# Generated by Django 3.2.23 on 2024-09-21 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Entertainment', '0006_video_games_music_film'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='category',
            field=models.ForeignKey(default='Entertainment', on_delete=django.db.models.deletion.CASCADE, to='Entertainment.categories'),
        ),
        migrations.AlterField(
            model_name='film',
            name='subcategory',
            field=models.ForeignKey(default='Film', on_delete=django.db.models.deletion.CASCADE, to='Entertainment.subcategories'),
        ),
        migrations.AlterField(
            model_name='music',
            name='category',
            field=models.ForeignKey(default='Entertainment', on_delete=django.db.models.deletion.CASCADE, to='Entertainment.categories'),
        ),
        migrations.AlterField(
            model_name='music',
            name='subcategory',
            field=models.ForeignKey(default='Music', on_delete=django.db.models.deletion.CASCADE, to='Entertainment.subcategories'),
        ),
        migrations.AlterField(
            model_name='subcategories',
            name='category',
            field=models.ForeignKey(default='Entertainment', on_delete=django.db.models.deletion.CASCADE, to='Entertainment.categories'),
        ),
        migrations.AlterField(
            model_name='video_games',
            name='category',
            field=models.ForeignKey(default='Entertainment', on_delete=django.db.models.deletion.CASCADE, to='Entertainment.categories'),
        ),
        migrations.AlterField(
            model_name='video_games',
            name='subcategory',
            field=models.ForeignKey(default='Video Games', on_delete=django.db.models.deletion.CASCADE, to='Entertainment.subcategories'),
        ),
    ]