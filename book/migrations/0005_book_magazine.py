# Generated by Django 3.0.4 on 2020-03-31 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_auto_20200329_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='magazine',
            field=models.BooleanField(default=False),
        ),
    ]