import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

from collections import defaultdict

# Predefined categories
CATEGORIES = {"movies", "games", "apps", "videos", "websites", "uncategorized"}
# Dictionary to store links by chat and category
links_by_chat = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm Zima Blue.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "<b>Commands:</b>\n"
        "/start - Start the bot\n"
        "/help - Show this help\n"
        "/listlinks - List all links\n"
        "/movies - Movie links\n"
        "/games - Game links\n"
        "/apps - App links\n"
        "/videos - Video links\n"
        "/websites - Website links\n"
        "/uncategorized - Uncategorized links",
        parse_mode="HTML"
    )

async def link_collector(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text.strip()
        chat_id = update.effective_chat.id
        # Ensure chat entry exists
        if chat_id not in links_by_chat:
            links_by_chat[chat_id] = {cat: [] for cat in CATEGORIES}
        # Check for batch category command: /category: <links> or /category <links>
        match = re.match(r"/(\w+):?\s*([\s\S]+)", text, re.DOTALL)
        if match:
            category = match.group(1).lower()
            if category in CATEGORIES:
                links_text = match.group(2)
                # Find all links, even if surrounded by text or on new lines
                links = re.findall(r'https?://[^\s)]+', links_text)
                filtered_links = [
                    link for link in links
                    if link not in links_by_chat[chat_id][category]
                ]
                already_present = [
                    link for link in links
                    if link in links_by_chat[chat_id][category]
                ]
                if filtered_links:
                    links_by_chat[chat_id][category].extend(filtered_links)
                    await update.message.delete()
                    return
                elif already_present:
                    await update.message.reply_text("Link already present in this category.")
                    return
        # Do not collect uncategorized links; ignore plain links
        # If not a link or category command, do nothing so unknown_command can handle it

async def category_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract the command (category) from the message, strip @botname if present
    command = update.message.text.strip().lower().lstrip("/")
    command = command.split("@", 1)[0]
    chat_id = update.effective_chat.id
    if chat_id not in links_by_chat:
        links_by_chat[chat_id] = {cat: [] for cat in CATEGORIES}
    if command in CATEGORIES:
        links = links_by_chat[chat_id].get(command, [])
        if links:
            formatted_links = "\n".join(f"<b>{idx+1}.</b> <a href=\"{link}\">{link}</a>" for idx, link in enumerate(links))
            await update.message.reply_text(
                f"<b>/{command}:</b>\n{formatted_links}",
                parse_mode="HTML",
                disable_web_page_preview=True
            )
        else:
            await update.message.reply_text(f"No links collected yet for /{command}.")
    else:
        await update.message.reply_text("Unknown category.")

async def list_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in links_by_chat:
        links_by_chat[chat_id] = {cat: [] for cat in CATEGORIES}
    messages = []
    for category in sorted(links_by_chat[chat_id].keys()):
        links = links_by_chat[chat_id][category]
        if links:
            command = f"/{category}:"
            formatted_links = "\n".join(f"<b>{idx+1}.</b> <a href=\"{link}\">{link}</a>" for idx, link in enumerate(links))
            messages.append(f"<b>{command}</b>\n{formatted_links}")
    if messages:
        await update.message.reply_text(
            "\n\n".join(messages),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text("No links collected yet.")

if __name__ == '__main__':
    # Load environment variables from .env file if present
    load_dotenv()
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable not set. Please set it in a .env file or as an environment variable.")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("listlinks", list_links))

    # Add a command for each category to get only that category's links, but only if the message is a pure command (no extra text)
    from telegram.ext import filters as tg_filters
    for cat in CATEGORIES:
        if cat != "uncategorized":
            # Accept /cat, /cat@bot, case-insensitive
            pattern = rf"(?i)^/{cat}(?:@\w+)?$"
            app.add_handler(CommandHandler(cat, category_links, filters=tg_filters.Regex(pattern)))

    # link_collector should handle /Movies (with or without colon) followed by links, i.e., not a pure command
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, link_collector))

    app.run_polling()
