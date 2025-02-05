# Generated by Django 4.0.10 on 2025-02-04 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0007_alter_evaluator_job_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formsection',
            name='form_subsections',
            field=models.ManyToManyField(related_name='form_subsections', to='data_management.formsubsection'),
        ),
        migrations.AlterField(
            model_name='onaform',
            name='ONA_sections',
            field=models.ManyToManyField(help_text='Selecione as seções que você quer ter no formulário. (A ordem importa!) --- ', related_name='ona_form_sections', to='data_management.formsection'),
        ),
        migrations.AlterField(
            model_name='onaform',
            name='form_title',
            field=models.CharField(help_text='Titulo para o formulário.', max_length=80),
        ),
        migrations.AlterField(
            model_name='onaform',
            name='hospital',
            field=models.ForeignKey(help_text='Indique o hospital ao qual este formulário está associado.', on_delete=django.db.models.deletion.CASCADE, to='data_management.hospital'),
        ),
    ]
