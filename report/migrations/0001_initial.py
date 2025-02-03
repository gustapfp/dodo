# Generated by Django 4.0.10 on 2025-02-03 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data_management', '0006_remove_formsubsectionanswered_answered_questions_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormSectionAnswered',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ONAFormAnswered',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answered_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('answered_sections', models.ManyToManyField(related_name='answered_sections', to='report.formsectionanswered')),
                ('evaluator', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='related_evaluator', to='data_management.evaluator')),
                ('ona_form', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='related_ona_form', to='data_management.onaform')),
            ],
            options={
                'verbose_name': 'Formulário ONA Respondido',
                'verbose_name_plural': 'Formulários ONA Respondidos',
            },
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=20, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answers', to='data_management.question')),
            ],
        ),
        migrations.CreateModel(
            name='ONAFormDistribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distribution', models.JSONField(default=dict)),
                ('total_distribution', models.FloatField(default=0.0)),
                ('score', models.FloatField(default=0.0, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('hospital', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='related_hospital_distribution', to='data_management.hospital')),
                ('ona_form', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='related_ona_form_distribution', to='report.onaformanswered')),
            ],
            options={
                'verbose_name': 'Distribuição ONA',
                'verbose_name_plural': 'Distribuições ONA',
            },
        ),
        migrations.CreateModel(
            name='FormSubsectionAnswered',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answered_questions_level_1', models.ManyToManyField(related_name='answered_questions_level_1', to='report.questionanswer')),
                ('answered_questions_level_2', models.ManyToManyField(related_name='answered_questions_level_2', to='report.questionanswer')),
                ('form_subsection', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='related_subsection', to='data_management.formsubsection')),
            ],
        ),
        migrations.AddField(
            model_name='formsectionanswered',
            name='answered_questions_level_3',
            field=models.ManyToManyField(related_name='answered_questions_level_3', to='report.questionanswer'),
        ),
        migrations.AddField(
            model_name='formsectionanswered',
            name='answered_subsections',
            field=models.ManyToManyField(related_name='answered_subsections', to='report.formsubsectionanswered'),
        ),
        migrations.AddField(
            model_name='formsectionanswered',
            name='form_section',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='related_section', to='data_management.formsection'),
        ),
    ]
