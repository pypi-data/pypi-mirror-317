import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

class DiscordNotifier:
    """A class to handle Discord webhook notifications.
    
    This class provides functionality to send messages to Discord channels
    through webhooks. It supports markdown formatting and can be configured
    either through environment variables or direct webhook URL.
    """
    
    def __init__(self, webhook_url: Optional[str] = None):
        """Initialize the Discord notifier.
        
        Args:
            webhook_url (str, optional): Direct webhook URL. If not provided,
                                       will try to load from .env file.
        """
        self.webhook_url = webhook_url
        
        if not self.webhook_url:
            root_dir = Path(__file__).parent.parent
            env_path = root_dir / '.env'
            load_dotenv(dotenv_path=env_path)
            self.webhook_url = os.getenv('WEBHOOK_URL')
            
        if not self.webhook_url:
            raise ValueError("Webhook URL is not provided and WEBHOOK_URL is not set in the .env file")

    def send_message(self, content: str, title: Optional[str] = None) -> bool:
        """Send a message to Discord via webhook.
        
        Args:
            content (str): The message content to send (supports markdown)
            title (str, optional): The title of the message
            
        Returns:
            bool: True if the message was sent successfully, False otherwise
            
        Example:
            >>> notifier = DiscordNotifier("your-webhook-url")
            >>> success = notifier.send_message("Hello, World!", "Greeting")
        """
        if not content:
            return False
            
        message = f"**{title}**\n{content}" if title else content
        
        try:
            response = requests.post(
                self.webhook_url,
                json={"content": message},
                timeout=10  # Add timeout for safety
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message: {str(e)}")
            return False 