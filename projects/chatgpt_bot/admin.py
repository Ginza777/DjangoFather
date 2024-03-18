# apps/your_app/admin.py

from django.contrib import admin

from .models import (
    Chat_mode,
    TelegramProfile,
    Config,
    Dialog,
    GptModels,
    Messages_dialog,
    Subscribtion,
    TextModel,
    TokenPackage, ChatGptTokens, TelegramBot
)


@admin.register(TextModel)
class TextModelAdmin(admin.ModelAdmin):
    list_display = ("name", "key")


@admin.register(Subscribtion)
class SubscribtionAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "n_tokens", "n_images", "n_tts")


@admin.register(TokenPackage)
class TokenPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "n_tokens", "n_images", "n_tts")


@admin.register(TelegramProfile)
class TelegramProfileUserAdmin(admin.ModelAdmin):
    list_display = (
        "id", "telegram_id", "first_name","last_name","username","last_interaction", "current_chat_mode", "current_model", "daily_limit", "extra_limit","language")
    filter_horizontal = ("bot",)
    search_fields = ("telegram_id", "first_name","last_name","username",)
    list_filter = ("current_chat_mode", "current_model", "language", "bot")


@admin.register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "chat_mode", "start_time", "gpt_model", "bot", "input_tokens", "output_tokens", "end")
    list_filter = ("chat_mode", "gpt_model", "end", "user__username")


@admin.register(Messages_dialog)
class MessagesDialogAdmin(admin.ModelAdmin):
    list_display = ("dialog_user__first_name","dialog__user__last_name","dialog_user__username", "user", "bot", "dialog", "input_tokens", "output_tokens", "end", 'chat_mode')
    list_filter = ("dialog__chat_mode", "dialog__gpt_model", "dialog__end")

    def dialog_user(self, obj):
        return obj.dialog.user

    dialog_user.short_description = "User"

    def chat_mode(self, obj):
        return obj.dialog.chat_mode

    chat_mode.short_description = "Chat Mode"


@admin.register(Chat_mode)
class ChatModeAdmin(admin.ModelAdmin):
    list_display = ("key", "model_name", "model_type", "parse_mode", "hidden", "created_at", "updated_at")


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = (
        "openai_api_base",
        "new_dialog_timeout",
        "return_n_generated_images",
        "n_chat_modes_per_page",
        "image_size",
        "enable_message_streaming",
        "chatgpt_price_per_1000_tokens",
        "gpt_price_per_1000_tokens",
        "whisper_price_per_1_min",
    )


@admin.register(GptModels)
class GptModelsAdmin(admin.ModelAdmin):
    list_display = ("model", "config")


@admin.register(ChatGptTokens)
class ChatGptTokensAdmin(admin.ModelAdmin):
    list_display = ("token",)


@admin.register(TelegramBot)
class LogSenderBotAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "bot_token",)
