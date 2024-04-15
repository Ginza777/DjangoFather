import os

from projects.chatgpt_bot.views import (
    help,
    language_choice_handle,
    message_handle,
    new_dialog_handle,
    set_chat_modes_callback_handle,
    settings_choice_handle,
    settings_handle,
    show_chat_modes,
    show_chat_modes_callback_handle,
    start,
    user_balance,
    about,
)

from django.conf import settings
from telegram import Bot, BotCommand
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)


async def post_init(application: Application):
    print("post_init function is called.")
    await application.bot.set_my_commands(
        [
            BotCommand("/start", "Start bot"),
            BotCommand("/new", "Start new dialog"),
            BotCommand("/mode", "Select chat mode"),
            BotCommand("/retry", "Re-generate response for previous query"),
            BotCommand("/balance", "Show balance"),
            BotCommand("/settings", "Show settings"),
            BotCommand("/help", "Show help message"),
        ]
    )


async def setup(token):
    print("chatgpt setup process...")
    persistence_file = os.path.join(settings.BASE_DIR, "media", "state_record", "conversationbot.pickle")
    persistence = PicklePersistence(filepath=persistence_file)
    bot = Bot(token=token)
    # await bot.initialize()
    application = (
        ApplicationBuilder()
        .token(token)
        .concurrent_updates(True)
        .http_version("1.1")
        .get_updates_http_version("1.1")
        .post_init(post_init)
        .persistence(persistence)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex(r"^Start$"), start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(MessageHandler(filters.Regex(r"^Help$"), help))
    application.add_handler(CommandHandler("mode", show_chat_modes))
    application.add_handler(MessageHandler(filters.Regex(r"^Chat_mode$"), show_chat_modes))
    application.add_handler(CommandHandler("balance", user_balance))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(MessageHandler(filters.Regex(r"^My_balance$"), user_balance))
    application.add_handler(CommandHandler("settings", settings_handle))
    application.add_handler(MessageHandler(filters.Regex(r"^Settings$"), settings_handle))
    application.add_handler(CommandHandler("new", new_dialog_handle))
    application.add_handler(MessageHandler(filters.Regex(r"^New_dialog$"), new_dialog_handle))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handle))

    # callback
    application.add_handler(CallbackQueryHandler(show_chat_modes_callback_handle, pattern="^show_chat_modes"))
    application.add_handler(CallbackQueryHandler(set_chat_modes_callback_handle, pattern="^set_chat_modes"))
    application.add_handler(CallbackQueryHandler(settings_choice_handle, pattern="^main_setting_"))
    application.add_handler(CallbackQueryHandler(language_choice_handle, pattern="^language_setting_"))
    application.add_handler(CallbackQueryHandler(settings_handle, pattern="^setting_back"))
    application.add_handler(CallbackQueryHandler(settings_handle, pattern="^delete_setting_back"))

    # await application.initialize()
    return application, bot
