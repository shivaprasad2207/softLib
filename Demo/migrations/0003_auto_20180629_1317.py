# Generated by Django 2.0.6 on 2018-06-29 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Demo', '0002_userauth_userinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registerorganisation',
            name='orgPassword',
        ),
        migrations.AddField(
            model_name='userauth',
            name='userPin',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]