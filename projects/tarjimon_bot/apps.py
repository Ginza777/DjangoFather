import asyncio
import traceback

import django.core.exceptions
import environ
import requests.exceptions
import telegram
from asgiref.sync import sync_to_async
from django.apps import AppConfig
from django.db.utils import ProgrammingError

from .utils.bot import set_webhook

env = environ.Env()
environ.Env.read_env()


class ChatgptBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "projects.tarjimon_bot"

    def ready(self):
        # call_command('migrate', interactive=False)
        asyncio.run(self.setup_webhook())

    async def setup_webhook(self):
        print("setup_webhook...")
        try:
            bot_tokens = await self.get_bot_tokens()
            print("bot_tokens: ", bot_tokens)
            for bot_token in bot_tokens:
                await set_webhook(bot_token)
        except telegram.error.RetryAfter:
            pass
        except requests.exceptions.ConnectionError:
            print("Connection error. Please check your internet connection.")
        except django.core.exceptions.ImproperlyConfigured:
            print("Improperly configured. Please check your settings.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()

    @sync_to_async
    def get_bot_tokens(self):
        try:
            from .models import TelegramBot
            bot_tokens = list(TelegramBot.objects.all().values_list("bot_token", flat=True))
        except ProgrammingError:
            bot_tokens = []

        return bot_tokens
