# Generated by Django 4.1.6 on 2024-11-28 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('displaysite', '0005_data_newest_update'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='newest_update',
            new_name='up_date',
        ),
    ]