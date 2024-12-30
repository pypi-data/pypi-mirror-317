# Discord Notifier

A simple Python package for sending notifications to Discord channels using webhooks.

## Installation

```bash
pip install dugudugu-discord-notifier
```

## Usage

```python
from notifier.discord_notifier import DiscordNotifier

# Initialize with webhook URL
webhook_url = "your-webhook-url-here"  # Discord webhook URL
notifier = DiscordNotifier(webhook_url)

# Send a simple message
notifier.send_message("Hello, World!")

# Send a message with title
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
- Timeout handling
- Error reporting

## Requirements

- Python 3.7+
- requests
