"""
Slack Notification Client

Posts messages to Slack via Incoming Webhook.
"""

import requests
import logging

logger = logging.getLogger(__name__)


class SlackClient:
    """Client for posting messages to Slack via Webhook."""
    
    def __init__(self, webhook_url: str) -> None:
        """
        Initialize SlackClient with webhook URL.
        
        Args:
            webhook_url: Slack Incoming Webhook URL
        """
        self.webhook_url = webhook_url
    
    def post_message(self, text: str) -> None:
        """
        Post a message to Slack via Webhook.
        
        Args:
            text: The message text to post
            
        Raises:
            requests.RequestException: If webhook request fails
        """
        payload = {"text": text}
        
        response = requests.post(
            self.webhook_url,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            logger.error(f"Slack webhook failed: {response.status_code} - {response.text}")
            response.raise_for_status()
        
        logger.info("Message posted to Slack successfully")
    
    def create_digest(self, papers: list[dict]) -> str:
        """
        Create a formatted digest message from a list of papers.
        
        Args:
            papers: List of paper dictionaries with title, link, upvotes, abstract
            
        Returns:
            Formatted string for Slack message
        """
        if not papers:
            return "📚 Weekly Top Papers from Hugging Face\n\nNo papers found this week."
        
        lines = ["📚 *Weekly Top Papers from Hugging Face*\n"]
        
        for i, paper in enumerate(papers, 1):
            title = paper.get("title", "Untitled")
            link = paper.get("link", "")
            upvotes = paper.get("upvotes", 0)
            abstract = paper.get("abstract", "")
            
            # Truncate abstract if too long
            if len(abstract) > 200:
                abstract = abstract[:197] + "..."
            
            lines.append(f"*{i}. {title}*")
            lines.append(f"   🔗 {link}")
            lines.append(f"   👍 {upvotes} upvotes")
            if abstract:
                lines.append(f"   > {abstract}")
            lines.append("")
        
        return "\n".join(lines)
