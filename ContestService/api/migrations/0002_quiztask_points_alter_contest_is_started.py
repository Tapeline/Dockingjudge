# Generated by Django 5.0.2 on 2024-08-30 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiztask',
            name='points',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contest',
            name='is_started',
            field=models.BooleanField(default=False),
        ),
    ]
