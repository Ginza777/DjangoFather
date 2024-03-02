# Generated by Django 5.0.1 on 2024-03-02 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatgpt_bot', '0005_alter_telegramprofile_current_chat_mode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='backupsenderbot',
            options={'verbose_name': 'BackupBot', 'verbose_name_plural': 'BackupBot'},
        ),
        migrations.AlterModelOptions(
            name='chat_mode',
            options={'verbose_name': 'ChatMode', 'verbose_name_plural': 'ChatMode'},
        ),
        migrations.AlterModelOptions(
            name='chatgpttokens',
            options={'verbose_name': 'GPTToken', 'verbose_name_plural': 'GPTToken'},
        ),
        migrations.AlterModelOptions(
            name='config',
            options={'verbose_name': 'Config', 'verbose_name_plural': 'Config'},
        ),
        migrations.AlterModelOptions(
            name='dialog',
            options={'verbose_name': 'Dialog', 'verbose_name_plural': 'Dialog'},
        ),
        migrations.AlterModelOptions(
            name='gptmodels',
            options={'verbose_name': 'GptModel', 'verbose_name_plural': 'GptModel'},
        ),
        migrations.AlterModelOptions(
            name='logsenderbot',
            options={'verbose_name': 'LogBot', 'verbose_name_plural': 'LogBot'},
        ),
        migrations.AlterModelOptions(
            name='messages_dialog',
            options={'verbose_name': 'MessagesDialog', 'verbose_name_plural': 'MessagesDialog'},
        ),
        migrations.AlterModelOptions(
            name='subscribtion',
            options={'verbose_name': 'Subscribtion', 'verbose_name_plural': 'Subscribtion'},
        ),
        migrations.AlterModelOptions(
            name='telegrambot',
            options={'verbose_name': 'TelegramBot', 'verbose_name_plural': 'TelegramBot'},
        ),
        migrations.AlterModelOptions(
            name='telegramprofile',
            options={'verbose_name': 'User', 'verbose_name_plural': 'User'},
        ),
        migrations.AlterModelOptions(
            name='tokenpackage',
            options={'verbose_name': 'TokenPackage', 'verbose_name_plural': 'TokenPackage'},
        ),
    ]
