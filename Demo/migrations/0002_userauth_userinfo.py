# Generated by Django 2.0.6 on 2018-06-28 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Demo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAuth',
            fields=[
                ('userId', models.AutoField(primary_key=True, serialize=False)),
                ('orgCode', models.CharField(blank=True, max_length=255)),
                ('userEmail', models.EmailField(blank=True, max_length=255)),
                ('userPassword', models.CharField(blank=True, max_length=255)),
                ('userRole', models.IntegerField(default=1)),
                ('is_active', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(blank=True, max_length=255)),
                ('lastName', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, max_length=255)),
                ('adress', models.CharField(blank=True, max_length=255)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Demo.UserAuth')),
            ],
        ),
    ]
