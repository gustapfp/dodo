# Generated by Django 4.0.10 on 2025-02-06 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0006_create_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluator',
            name='email',
            field=models.EmailField(max_length=80),
        ),
    ]
