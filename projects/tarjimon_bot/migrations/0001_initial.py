# Generated by Django 5.0.1 on 2024-03-02 21:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('bot_token', models.CharField(max_length=255, unique=True)),
                ('bot_username', models.CharField(blank=True, max_length=125, null=True)),
                ('extra_field', models.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'TelegramBot',
                'verbose_name_plural': 'TelegramBot',
            },
        ),
        migrations.CreateModel(
            name='TelegramProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.PositiveBigIntegerField(unique=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('language', models.CharField(choices=[('uz', 'Uzbek'), ('en', 'English'), ('ru', 'Russian'), ('es', 'Spanish'), ('fr', 'French'), ('de', 'German')], default='uz', max_length=255, null=True)),
                ('is_bot', models.BooleanField(default=False)),
                ('user_token', models.UUIDField(blank=True, null=True, unique=True)),
                ('native_language', models.CharField(blank=True, default='no_lang', max_length=10, null=True)),
                ('target_language', models.CharField(blank=True, default='no_lang', max_length=10, null=True)),
                ('bot', models.ManyToManyField(to='tarjimon_bot.telegrambot')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'User',
            },
        ),
        migrations.CreateModel(
            name='TranslatorConversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('translated_text', models.TextField()),
                ('source_language', models.CharField(blank=True, max_length=10, null=True)),
                ('target_language', models.CharField(blank=True, max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tarjimon_bot.telegramprofile')),
            ],
        ),
    ]
