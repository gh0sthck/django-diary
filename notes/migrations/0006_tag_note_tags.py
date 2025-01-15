# Generated by Django 5.1.4 on 2025-01-15 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_alter_note_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['-name'],
            },
        ),
        migrations.AddField(
            model_name='note',
            name='tags',
            field=models.ManyToManyField(to='notes.tag'),
        ),
    ]
