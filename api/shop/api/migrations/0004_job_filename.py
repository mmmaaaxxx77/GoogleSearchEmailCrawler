# Generated by Django 2.0.7 on 2018-10-15 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20181015_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='filename',
            field=models.CharField(default='', max_length=50),
        ),
    ]
