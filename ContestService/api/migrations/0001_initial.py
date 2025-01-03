# Generated by Django 5.0.2 on 2024-08-06 21:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('author', models.IntegerField()),
                ('description', models.TextField()),
                ('is_started', models.BooleanField(default=True)),
                ('is_ended', models.BooleanField(default=False)),
                ('time_limit_seconds', models.IntegerField(default=-1)),
                ('pages', models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name='CodeTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('test_suite', models.JSONField()),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.contest')),
            ],
        ),
        migrations.CreateModel(
            name='ContestSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.contest')),
            ],
        ),
        migrations.CreateModel(
            name='QuizTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('validator', models.JSONField(default={})),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.contest')),
            ],
        ),
        migrations.CreateModel(
            name='TextPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('is_enter_page', models.BooleanField(default=False)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.contest')),
            ],
        ),
    ]
