# Generated by Django 5.1.3 on 2024-11-29 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affirmations_app', '0006_userrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affirmation',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
