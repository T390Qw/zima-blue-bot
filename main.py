import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
        if chat_id not in links_by_chat:
            links_by_chat[chat_id] = {cat: [] for cat in CATEGORIES}

        match = re.match(r"/(\w+):?\s*([\s\S]+)", text, re.DOTALL)
        if match:
            category = match.group(1).lower()
            if category in CATEGORIES:
                links_text = match.group(2)
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

async def category_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

if __name__ == "__main__":
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    webhook_url = os.environ.get("WEBHOOK_URL")  # This will be your Render URL

    if not token or not webhook_url:
        raise RuntimeError("TELEGRAM_BOT_TOKEN and WEBHOOK_URL must be set as environment variables.")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("listlinks", list_links))

    for cat in CATEGORIES:
        if cat != "uncategorized":
            pattern = rf"(?i)^/{cat}(?:@\w+)?$"
            app.add_handler(CommandHandler(cat, category_links, filters.Regex(pattern)))

    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, link_collector))

    # Run webhook instead of polling
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        url_path=token,
        webhook_url=f"{webhook_url}/{token}"
    )
