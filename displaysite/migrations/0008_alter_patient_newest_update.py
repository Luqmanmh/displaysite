# Generated by Django 4.1.6 on 2024-12-01 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('displaysite', '0007_alter_patient_newest_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='newest_update',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
