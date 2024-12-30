# Discord Notifier

A simple Python package for sending notifications to Discord channels using webhooks.

## Installation

```bash
pip install dugudugu-discord-notifier
```

## Usage

There are two ways to use this notifier:

### Method 1: Direct webhook URL

```python
from notifier.discord_notifier import DiscordNotifier

# Initialize with webhook URL
notifier = DiscordNotifier("your-webhook-url-here")

# Send messages
notifier.send_message("Hello, World!")
notifier.send_message("This is the message content", "This is the title")
```

### Method 2: Using environment variables

1. Create a `.env` file in your project root directory
2. Add your Discord webhook URL to the `.env` file:
   ```env
   WEBHOOK_URL=your_discord_webhook_url_here
   ```
3. Use the notifier:
   ```python
   from notifier.discord_notifier import DiscordNotifier

   # Initialize (will read from .env file)
   notifier = DiscordNotifier()

   # Send messages
   notifier.send_message("Hello, World!")
   notifier.send_message("This is the message content", "This is the title")
   ```

### How to get Discord Webhook URL:
1. Go to your Discord server
2. Right-click on the channel you want to send messages to
3. Click 'Edit Channel'
4. Click 'Integrations'
5. Click 'Create Webhook' (or 'View Webhooks' if you already have one)
6. Click 'New Webhook'
7. Copy the Webhook URL

## Features

- Simple and easy to use
- Supports markdown formatting
- Flexible configuration (direct URL or environment variables)
- Timeout handling
- Error reporting

## Requirements

- Python 3.7+
- requests
- python-dotenv
