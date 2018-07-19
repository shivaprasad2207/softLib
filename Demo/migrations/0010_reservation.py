# Generated by Django 2.0.6 on 2018-07-14 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Demo', '0009_bookcopy_is_reserved'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reservationId', models.AutoField(primary_key=True, serialize=False)),
                ('bookCopyCode', models.CharField(blank=True, max_length=255)),
                ('orgCode', models.CharField(blank=True, max_length=255)),
                ('dateFrom', models.DateField()),
                ('dateTo', models.DateField()),
                ('is_active', models.IntegerField(default=1)),
                ('is_reserved', models.IntegerField(default=0)),
                ('bookCopyId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Demo.BookCopy')),
                ('userAuthId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Demo.UserAuth')),
            ],
        ),
    ]
