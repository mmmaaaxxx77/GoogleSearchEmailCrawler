# Generated by Django 2.0.7 on 2018-10-15 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20181015_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='skip_url',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
