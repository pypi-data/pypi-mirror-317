import requests
from typing import Optional

class DiscordNotifier:
    """A class to handle Discord webhook notifications.
    
    This class provides functionality to send messages to Discord channels
    through webhooks. It supports markdown formatting.
    """
    
    def __init__(self, webhook_url: str):
        """Initialize the Discord notifier.
        
        Args:
            webhook_url (str): Discord webhook URL
        """
        if not webhook_url:
            raise ValueError("Webhook URL must be provided")
            
        self.webhook_url = webhook_url

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