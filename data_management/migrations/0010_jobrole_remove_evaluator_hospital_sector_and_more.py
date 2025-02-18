# Generated by Django 4.0.10 on 2025-02-18 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0009_remove_onaform_evaluator'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'verbose_name': 'Cargo',
                'verbose_name_plural': 'Cargos',
            },
        ),
        migrations.RemoveField(
            model_name='evaluator',
            name='hospital_sector',
        ),
        migrations.AddField(
            model_name='evaluator',
            name='hospital_sector',
            field=models.ManyToManyField(related_name='evaluator_sectors', to='data_management.sector'),
        ),
        migrations.RemoveField(
            model_name='evaluator',
            name='job_role',
        ),
        migrations.AddField(
            model_name='evaluator',
            name='job_role',
            field=models.ManyToManyField(related_name='evaluator_job_role', to='data_management.jobrole'),
        ),
    ]
