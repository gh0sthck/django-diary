# Generated by Django 5.1.4 on 2025-01-16 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_tag_note_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='slug',
            field=models.SlugField(max_length=128, verbose_name='Слаг'),
        ),
    ]
