# Generated by Django 4.0.10 on 2025-01-13 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0004_formsection_level3_formsection_section_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formsection',
            old_name='level3',
            new_name='questions_level3',
        ),
        migrations.RenameField(
            model_name='formsection',
            old_name='sections_title',
            new_name='section_title',
        ),
        migrations.RenameField(
            model_name='formsubsection',
            old_name='level1',
            new_name='questions_level1',
        ),
        migrations.RenameField(
            model_name='formsubsection',
            old_name='level2',
            new_name='questions_level2',
        ),
        migrations.RemoveField(
            model_name='formsubsection',
            name='questions',
        ),
        migrations.RemoveField(
            model_name='question',
            name='level',
        ),
        migrations.RemoveField(
            model_name='question',
            name='result',
        ),
    ]
