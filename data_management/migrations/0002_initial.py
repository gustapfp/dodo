# Generated by Django 4.0.10 on 2025-02-19 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='username',
            field=models.OneToOneField(max_length=80, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='formsubsection',
            name='questions_level1',
            field=models.ManyToManyField(related_name='level1_questions', to='data_management.question'),
        ),
        migrations.AddField(
            model_name='formsubsection',
            name='questions_level2',
            field=models.ManyToManyField(related_name='level2_questions', to='data_management.question'),
        ),
        migrations.AddField(
            model_name='formsection',
            name='form_subsections',
            field=models.ManyToManyField(related_name='form_subsections', to='data_management.formsubsection'),
        ),
        migrations.AddField(
            model_name='formsection',
            name='questions_level3',
            field=models.ManyToManyField(related_name='level3_questions', to='data_management.question'),
        ),
        migrations.AddField(
            model_name='evaluator',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_management.hospital'),
        ),
        migrations.AddField(
            model_name='evaluator',
            name='hospital_sector',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='evaluator_sectors', to='data_management.sector'),
        ),
        migrations.AddField(
            model_name='evaluator',
            name='job_role',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='evaluator_job_role', to='data_management.jobroles'),
        ),
    ]
