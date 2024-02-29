# Generated by Django 5.0.1 on 2024-02-29 12:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theses', '0002_alter_academicmanager_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='student',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='student',
            name='thesis',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='students', to='theses.thesis', unique=True),
        ),
    ]