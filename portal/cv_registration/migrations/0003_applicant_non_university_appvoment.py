# Generated by Django 2.2.11 on 2020-03-20 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv_registration', '0002_auto_20200319_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='non_university_appvoment',
            field=models.CharField(choices=[('Approved', 'Approved'), ('DisApproved', 'DisApproved'), ('Pending', 'Pending')], default='Pending', max_length=14),
        ),
    ]