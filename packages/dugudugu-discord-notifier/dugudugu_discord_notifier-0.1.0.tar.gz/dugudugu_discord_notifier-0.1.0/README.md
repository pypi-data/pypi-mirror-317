# Discord Notifier

A simple Python package for sending notifications to Discord channels using webhooks.

## Installation

```bash
pip install discord-notifier
```

Or install from source:

```bash
git clone https://github.com/yourusername/discord-notifier.git
cd discord-notifier
pip install .
```

## Configuration

1. Copy `.env.template` to `.env`
2. Add your Discord webhook URL to the `.env` file

## Usage

```python
from notifier.discord_notifier import DiscordNotifier

# Initialize the notifier
notifier = DiscordNotifier()

# Send a simple message
notifier.send_message("Hello, World!")

# Send a message with a title
notifier.send_message("This is the message content", "This is the title")
```

## Features

- Simple and easy to use
- Supports markdown formatting
- Environment-based configuration
- Timeout handling
- Error reporting

## Requirements

- Python 3.7+
- requests
- python-dotenv
