import uuid

from django.db import models

from .utils.bot import get_info, set_webhook_sync

AVAILABLE_TEXT_MODELS_CHOICES = [
    ("gpt-3.5-turbo", "GPT-3.5 Turbo"),
    ("gpt-3.5-turbo-16k", "GPT-3.5 Turbo 16k"),
    ("gpt-4-1106-preview", "GPT-4 1106 Preview"),
    ("gpt-4", "GPT-4"),
    ("text-davinci-003", "Text Davinci 003"),
]


class Language(models.TextChoices):
    UZBEK = "uz", "Uzbek"
    ENGLISH = "en", "English"
    RUSSIAN = "ru", "Russian"
    SPANISH = "es", "Spanish"
    FRENCH = "fr", "French"
    GERMAN = "de", "German"


class TelegramBot(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    bot_token = models.CharField(max_length=255, unique=True)
    bot_username = models.CharField(max_length=125, blank=True, null=True)
    extra_field = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        set_webhook_sync(self.bot_token)
        username, name = get_info(bot_token=self.bot_token)
        self.bot_username = username
        self.name = name

        super(TelegramBot, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "TelegramBot"
        verbose_name_plural = "TelegramBot"


class BackupSenderBot(models.Model):
    token = models.CharField(max_length=200, unique=True)
    channel_id = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.channel_id.startswith('-'):
            if self.channel_id.startswith('100'):
                self.channel_id = '-' + self.channel_id
            else:
                self.channel_id = '-100' + self.channel_id

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "BackupBot"
        verbose_name_plural = "BackupBot"


class Chat_mode(models.Model):
    key = models.CharField(max_length=200)
    model_name = models.CharField(max_length=200)
    model_type = models.CharField(max_length=200, null=True, blank=True)
    welcome_message = models.TextField()
    prompt_start = models.TextField(null=True, blank=True)
    parse_mode = models.CharField(max_length=200, null=True, blank=True, default="html")
    extra_field = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.model_name

    class Meta:
        verbose_name = "ChatMode"
        verbose_name_plural = "ChatMode"
        db_table = "chat_mode"


class GptModels(models.Model):
    model = models.CharField(max_length=200, unique=True)
    config = models.JSONField()

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "GptModel"
        verbose_name_plural = "GptModel"
        db_table = "gpt_models"


class TextModel(models.Model):
    name = models.CharField(max_length=200, unique=True)
    key = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Text Model"
        verbose_name_plural = "Text Models"
        db_table = "text_model"
        unique_together = ("name", "key")


class Subscribtion(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.FloatField()
    n_tokens = models.IntegerField()
    n_images = models.IntegerField()
    n_tts = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subscribtion"
        verbose_name_plural = "Subscribtion"
        db_table = "subscribtion"


class TokenPackage(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.FloatField()
    n_tokens = models.IntegerField()
    n_images = models.IntegerField()
    n_tts = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "TokenPackage"
        verbose_name_plural = "TokenPackage"
        db_table = "token_package"


class TelegramProfile(models.Model):
    class Language(models.TextChoices):
        UZBEK = "uz", "Uzbek"
        ENGLISH = "en", "English"
        RUSSIAN = "ru", "Russian"
        SPANISH = "es", "Spanish"
        FRENCH = "fr", "French"
        GERMAN = "de", "German"

    bot = models.ManyToManyField(TelegramBot)
    telegram_id = models.PositiveBigIntegerField(unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, choices=Language.choices, default=Language.UZBEK, null=True)
    is_bot = models.BooleanField(default=False)
    last_interaction = models.DateTimeField(auto_now=True)
    first_seen = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    current_chat_mode = models.ForeignKey(Chat_mode, on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name="current_chat_mode")
    current_model = models.ForeignKey(GptModels, on_delete=models.SET_NULL, null=True, blank=True)
    n_used_tokens = models.PositiveBigIntegerField(null=True, blank=True)
    n_generated_images = models.IntegerField(default=0, null=True, blank=True)
    n_transcribed_seconds = models.IntegerField(default=0, null=True, blank=True)
    user_allowed = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    user_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    language_choice = models.CharField(max_length=255, choices=Language.choices, default=Language.UZBEK, null=True)
    daily_limit = models.IntegerField(default=10, null=True, blank=True)
    extra_limit = models.IntegerField(default=0, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.user_token:
            self.user_token = uuid.uuid4()
        super(TelegramProfile, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"


class Dialog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(TelegramProfile, on_delete=models.SET_NULL, verbose_name="ChatGpt User", null=True,
                             blank=True)
    chat_mode = models.ForeignKey(Chat_mode, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    gpt_model = models.ForeignKey(GptModels, on_delete=models.SET_NULL, null=True, blank=True)
    bot = models.ForeignKey(TelegramBot, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    input_tokens = models.IntegerField(default=0)
    output_tokens = models.IntegerField(default=0)
    end = models.BooleanField(default=False)

    def __str__(self):
        return str(f"{self.user.telegram_id}---{self.id}")

    class Meta:
        verbose_name = "Dialog"
        verbose_name_plural = "Dialog"
        db_table = "dialog"


class Messages_dialog(models.Model):
    user = models.TextField(null=True, blank=True)
    bot = models.TextField(null=True, blank=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, null=True, blank=True, related_name="messages_dialog")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    msg_token = models.CharField(max_length=255, null=True, blank=True)
    input_tokens = models.IntegerField(default=0)
    output_tokens = models.IntegerField(default=0)
    end = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.msg_token:
            self.user_token = uuid.uuid4()
        super(Messages_dialog, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "MessagesDialog"
        verbose_name_plural = "MessagesDialog"
        db_table = "messages_dialog"


class Config(models.Model):
    openai_api_base = models.CharField(null=True, blank=True, max_length=200)
    new_dialog_timeout = models.IntegerField(null=True, blank=True, default=600)
    return_n_generated_images = models.IntegerField(default=1)
    n_chat_modes_per_page = models.IntegerField(default=5)
    image_size = models.CharField(max_length=200, default="512x512")
    enable_message_streaming = models.BooleanField(default=True)
    chatgpt_price_per_1000_tokens = models.FloatField(default=0.006)
    gpt_price_per_1000_tokens = models.FloatField(default=0.002)
    whisper_price_per_1_min = models.FloatField(default=0.006)
    extra_field = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Config"

    class Meta:
        verbose_name = "Config"
        verbose_name_plural = "Config"


class ChatGptTokens(models.Model):
    login = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200, unique=True)
    token = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "GPTToken"
        verbose_name_plural = "GPTToken"

