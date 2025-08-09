# Zima Blue - Telegram Link Collection Bot

A sophisticated Telegram bot designed for collecting and organizing links across multiple categories. Built with Python using the python-telegram-bot library, this bot provides an elegant solution for managing shared resources in group chats.

## Features

- **Multi-Category Link Management**: Organize links into predefined categories
- **Smart Link Detection**: Automatically detects and categorizes URLs
- **Duplicate Prevention**: Prevents duplicate links within categories
- **Rich Formatting**: Beautiful HTML-formatted responses with clickable links
- **Group Chat Optimized**: Designed specifically for group chat environments
- **Webhook Support**: Production-ready with webhook deployment
- **Environment Configuration**: Secure token management with .env files

## Categories Supported

- **Movies** - `/movies` - Movie streaming and download links
- **Games** - `/games` - Game downloads and resources
- **Apps** - `/apps` - Software applications and tools
- **Videos** - `/videos` - Video content links
- **Websites** - `/websites` - Useful websites and resources
- **Uncategorized** - `/uncategorized` - Links without specific category

## Prerequisites

- Python 3.7 or higher
- A Telegram Bot Token (obtain from [@BotFather](https://t.me/BotFather))
- A webhook URL (for production deployment)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/zima-blue-telegram-bot.git
cd zima-blue-telegram-bot
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

### 4. Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your configuration:
```bash
TELEGRAM_BOT_TOKEN=your-actual-bot-token-here
WEBHOOK_URL=https://your-app-name.onrender.com
PORT=8080
```

## Usage

### Running the Bot

#### Development (Polling Mode)
For development, you can modify the code to use polling instead of webhooks:

```python
# Replace the webhook section with:
# app.run_polling()
```

#### Production (Webhook Mode)
```bash
python main.py
```

### Bot Commands

#### User Commands
- `/start` - Welcome message and bot introduction
- `/help` - Display all available commands and usage instructions
- `/listlinks` - Show all collected links organized by category

#### Category Commands
- `/movies` - Display all movie links
- `/games` - Display all game links
- `/apps` - Display all app links
- `/videos` - Display all video links
- `/websites` - Display all website links
- `/uncategorized` - Display uncategorized links

### Adding Links

In group chats, add links using the format:
```
/category: https://example.com/link
```

Examples:
```
/movies: https://netflix.com/movie123
/games: https://store.steampowered.com/app/12345
/apps: https://apps.apple.com/app/id123456
```

The bot will:
1. Detect the category from the command
2. Extract all URLs from the message
3. Add unique links to the category
4. Delete the original message to keep chat clean
5. Notify if links already exist in the category

## Project Structure

```
zima-blue-telegram-bot/
├── main.py              # Main bot application with all handlers
├── requirements.txt     # Python dependencies (telegram-bot + webhooks)
├── .env.example        # Environment variables template
├── .env                # Your environment variables (create from .env.example)
├── .venv/              # Virtual environment (auto-generated)
└── README.md           # This file
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from @BotFather | Yes | - |
| `WEBHOOK_URL` | Your webhook URL for production | Yes | - |
| `PORT` | Port for webhook server | No | 8080 |

### Customization

#### Adding New Categories
1. Add the category to the `CATEGORIES` set in `main.py`:
```python
CATEGORIES = {"movies", "games", "apps", "videos", "websites", "uncategorized", "newcategory"}
```

2. The bot will automatically handle the new category with `/newcategory` command

#### Modifying Link Detection
The regex pattern for link detection can be adjusted in the `link_collector` function:
```python
links = re.findall(r'https?://[^\s)]+', links_text)
```

## Development

### Architecture Overview

- **Application**: Main bot instance with webhook configuration
- **Command Handlers**: Process slash commands
- **Message Handler**: Processes category-based link submissions
- **Regex Patterns**: Flexible command matching with username support
- **In-Memory Storage**: Links stored per chat ID (resets on restart)

### Key Components

1. **Link Collection System**:
   - Regex-based category detection
   - URL extraction and validation
   - Duplicate prevention
   - Automatic message cleanup

2. **Response Formatting**:
   - HTML-formatted messages
   - Numbered lists with clickable links
   - Web preview disabled for cleaner appearance

3. **Group Chat Optimization**:
   - Commands work with or without bot username
   - Case-insensitive command matching
   - Per-chat data isolation

### Error Handling

- Missing environment variable validation
- Invalid category handling
- Malformed URL detection
- Graceful error responses

## Deployment

### Render Deployment (Recommended)

1. **Create Web Service**:
   - Connect your GitHub repository
   - Set runtime to Python
   - Use `python main.py` as start command

2. **Environment Variables**:
   - Add `TELEGRAM_BOT_TOKEN`
   - Add `WEBHOOK_URL` (your Render app URL)
   - Add `PORT` (Render will provide this)

3. **Set Webhook**:
   ```bash
   curl -F "url=https://your-app.onrender.com/YOUR_BOT_TOKEN" \
        https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook
   ```

### Heroku Deployment

1. Create `Procfile`:
```
web: python main.py
```

2. Deploy with Heroku CLI:
```bash
heroku create your-bot-name
heroku config:set TELEGRAM_BOT_TOKEN=your-token
heroku config:set WEBHOOK_URL=https://your-bot-name.herokuapp.com
git push heroku main
```

### VPS/Cloud Deployment

1. **Using systemd** (Ubuntu/Debian):
```ini
[Unit]
Description=Zima Blue Telegram Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/path/to/zima-blue-telegram-bot
Environment="TELEGRAM_BOT_TOKEN=your-token"
Environment="WEBHOOK_URL=https://your-domain.com"
Environment="PORT=8080"
ExecStart=/path/to/zima-blue-telegram-bot/.venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

2. **Using Docker**:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## Troubleshooting

### Common Issues

1. **"TELEGRAM_BOT_TOKEN and WEBHOOK_URL must be set"**
   - Ensure both environment variables are properly set
   - Check `.env` file exists and is loaded

2. **Bot not responding in groups**
   - Ensure bot has admin permissions or can read messages
   - Check if privacy mode is disabled for group chats
   - Verify webhook is properly set

3. **Links not being collected**
   - Ensure correct format: `/category: https://link.com`
   - Check if links are already in the category
   - Verify bot has permission to delete messages

4. **Webhook issues**
   - Ensure webhook URL is publicly accessible
   - Check if URL ends with `/YOUR_BOT_TOKEN`
   - Verify SSL certificate (required for webhooks)

### Debug Mode

Enable debug logging by adding to `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

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

### Development Guidelines

- Follow PEP 8 style guidelines
- Add appropriate error handling
- Test in group chat environments
- Update documentation for new features

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for the excellent Python wrapper
- Telegram for providing the Bot API
- The Zima Blue concept for inspiration in elegant simplicity