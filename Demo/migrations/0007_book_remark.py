# Generated by Django 2.0.6 on 2018-07-04 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Demo', '0006_book_bookcopy'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='remark',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
