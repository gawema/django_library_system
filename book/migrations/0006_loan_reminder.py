# Generated by Django 3.0.4 on 2020-04-01 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_book_magazine'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='reminder',
            field=models.CharField(default='', max_length=500),
        ),
    ]
