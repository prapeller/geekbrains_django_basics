# Generated by Django 3.2.7 on 2021-10-17 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female')], max_length=1, verbose_name='gender'),
        ),
    ]