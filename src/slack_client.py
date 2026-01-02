import requests
import json
import os

class SlackClient:
    """
    Client for posting messages to Slack via Webhook.
    """

    def __init__(self, webhook_url: str):
        """
        Initializes the SlackClient.

        Args:
            webhook_url (str): The Slack Webhook URL.
        """
        # TODO: Store the webhook_url
        pass

    def post_message(self, text: str) -> None:
        """
        Posts a simple text message to Slack.

        Args:
            text (str): The message text to post.
        
        Raises:
            Exception: If the request to Slack fails.
        """
        # TODO: Construct the payload (JSON) with the 'text' field
        # TODO: Send a POST request to the webhook_url with the payload
        # TODO: Check the response status code. If not 200, raise an exception or log error.
        pass

    def create_digest(self, papers: list[dict]) -> str:
        """
        Formats a list of papers into a readable digest string for Slack.

        Args:
            papers (list[dict]): List of paper dictionaries (from ArxivClient).

        Returns:
            str: The formatted message string.
        """
        # TODO: Initialize an empty string or list for the message
        # TODO: Add a header (e.g., "DAILY ARXIV DIGEST")
        # TODO: Iterate through the papers
        # TODO: For each paper, append the title (as a link if possible), date, and a brief summary
        # TODO: Separate entries with newlines or dividers
        # TODO: Join the parts into a single string and return
        pass
