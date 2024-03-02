import datetime
import subprocess
import environ
import os


from .views import send_to_telegram
from apps.bot_main_setup.models import BackupSenderBot

env = environ.Env()
env.read_env(".env")


# Corrected class name to "Commands"


def backup_database():
    DB_NAME = env.str("DB_NAME")
    DB_USER = env.str("DB_USER")
    DB_PASSWORD = env.str("DB_PASSWORD")
    DB_HOST = env.str("DB_HOST")
    DB_PORT = env.str("DB_PORT")

    dump_file = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

    # Dumpni olish uchun bash komandasi
    command = f"pg_dump -U {DB_USER} -h {DB_HOST} -p {DB_PORT} {DB_NAME} > {dump_file}"
    os.environ['PGPASSWORD'] = DB_PASSWORD
    # Komandani bajarish
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing command: {e}")
        return
    if BackupSenderBot.objects.all().count() > 0:
        token = BackupSenderBot.objects.last().token
        channel_id = BackupSenderBot.objects.last().channel_id
    else:
        token = "6567332198:AAHRaGT5xLJdsJbWkugqgSJHbPGi8Zr2_ZI"
        channel_id = -1002041724232

    send_to_telegram(token, channel_id, dump_file, f"All bots: > Backup file: {dump_file}")
