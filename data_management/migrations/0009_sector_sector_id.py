# Generated by Django 4.0.10 on 2025-02-18 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0008_insert_job_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='sector',
            name='sector_id',
            field=models.CharField(default=None, max_length=80, null=True),
        ),
    ]
