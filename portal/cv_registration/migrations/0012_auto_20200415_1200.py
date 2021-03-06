# Generated by Django 2.2.11 on 2020-04-15 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv_registration', '0011_auto_20200415_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='attachment_type',
            field=models.CharField(choices=[('CV', 'CV'), ('Research Proposal', 'motivation_statement'), ('NIDA', 'NIDA'), ('Nomination letter', 'nomination_letter'), ('Project references', 'Project References'), ('Reference Letter', 'Reference Letter'), ('Research contributions', 'Research Contributions'), ('Research Proposal', 'research_proposal'), ('University Transcript', 'university_transcript'), ('Other', 'Other')], default='Other', max_length=14),
        ),
    ]
