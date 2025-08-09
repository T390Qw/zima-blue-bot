# Telegram Bot

A simple and functional Telegram bot built with Python using the python-telegram-bot library. This bot provides basic command handling and message responses, serving as a foundation for more complex Telegram bot applications.

## Features

- **Command Handling**: Responds to `/start`, `/help`, and `/list` commands
- **Message Processing**: Handles text messages and provides appropriate responses
- **Environment Configuration**: Uses `.env` files for secure token management
- **Error Handling**: Includes comprehensive error handling and logging
- **Extensible Structure**: Clean architecture for easy feature additions

## Prerequisites

- Python 3.7 or higher
- A Telegram Bot Token (obtain from [@BotFather](https://t.me/BotFather))

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/telegram_bot.git
cd telegram_bot
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: The `requirements.txt` includes `python-dotenv`. You'll also need to install the main telegram bot library:

```bash
pip install python-telegram-bot
```

### 4. Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Telegram bot token:
```bash
TELEGRAM_BOT_TOKEN=your-actual-bot-token-here
```

## Usage

### Running the Bot

```bash
python main.py
```

The bot will start and begin polling for messages. You'll see output indicating the bot is running.

### Available Commands

- `/start` - Welcome message and bot introduction
- `/help` - Display available commands and usage instructions
- `/list` - Show a list of items (customizable)

### Testing the Bot

1. Start a chat with your bot on Telegram
2. Send `/start` to see the welcome message
3. Try `/help` for command information
4. Send any text message to see the echo response

## Project Structure

```
telegram_bot/
├── main.py              # Main bot application
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .env                # Your environment variables (create from .env.example)
├── .venv/              # Virtual environment (auto-generated)
└── README.md           # This file
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from @BotFather | Yes |

### Customization

To add new commands:

1. Add a new handler function in `main.py`:
```python
async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Your response here")
```

2. Register the handler in the main function:
```python
app.add_handler(CommandHandler("newcommand", new_command))
```

## Development

### Adding New Features

The bot uses the python-telegram-bot library v20+ with asyncio. Key components:

- **Application**: Main bot instance
- **CommandHandler**: Handles slash commands
- **MessageHandler**: Processes text messages
- **Filters**: Controls which messages to process

### Error Handling

The bot includes comprehensive error handling:
- Missing token validation
- Network error recovery
- User-friendly error messages

### Logging

Logs are output to the console for debugging purposes. You can modify the logging level in `main.py` if needed.

## Deployment

### Local Development

For local development, simply run:
```bash
python main.py
```

### Production Deployment

For production deployment, consider:

1. **Using a process manager** like systemd, PM2, or supervisor
2. **Setting up webhooks** instead of polling for better performance
3. **Using environment variables** for configuration
4. **Setting up logging** to files instead of console

Example systemd service:
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/path/to/telegram_bot
Environment="TELEGRAM_BOT_TOKEN=your-token"
ExecStart=/path/to/telegram_bot/.venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Troubleshooting

### Common Issues

1. **"TELEGRAM_BOT_TOKEN environment variable not set"**
   - Ensure your `.env` file exists and contains the token
   - Verify the token is correct

2. **Import errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt` again

3. **Bot not responding**
   - Check if the bot is started
   - Verify the bot token is valid
   - Check if the bot has permission to read messages

### Getting Help

- Check the [python-telegram-bot documentation](https://docs.python-telegram-bot.org/)
- Review the [Telegram Bot API documentation](https://core.telegram.org/bots/api)
- Open an issue on GitHub for bugs or feature requests

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for the excellent Python wrapper
- Telegram for providing the Bot API