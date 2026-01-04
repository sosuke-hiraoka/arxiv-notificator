"""Tests for SlackClient."""

import pytest
from unittest.mock import MagicMock, patch

from slack_client import SlackClient


@pytest.fixture
def client():
    return SlackClient("https://hooks.slack.com/services/test/webhook")


def test_post_message_success(client):
    """Test successful message posting."""
    with patch('slack_client.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Should not raise
        client.post_message("Hello, Slack!")
        
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[1]["json"] == {"text": "Hello, Slack!"}


def test_post_message_failure(client):
    """Test message posting failure handling."""
    with patch('slack_client.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        mock_post.return_value = mock_response
        
        with pytest.raises(Exception):
            client.post_message("Hello, Slack!")


def test_webhook_url_stored(client):
    """Test that webhook URL is stored correctly."""
    assert client.webhook_url == "https://hooks.slack.com/services/test/webhook"


def test_create_digest_formats_papers(client):
    """Test that create_digest formats papers correctly."""
    papers = [
        {
            "title": "Test Paper",
            "link": "https://huggingface.co/papers/test",
            "upvotes": 100,
            "abstract": "This is a test abstract."
        }
    ]
    
    digest = client.create_digest(papers)
    
    assert "📚" in digest
    assert "Weekly Top Papers" in digest
    assert "*1. Test Paper*" in digest
    assert "https://huggingface.co/papers/test" in digest
    assert "100 upvotes" in digest
    assert "This is a test abstract." in digest


def test_create_digest_empty_list(client):
    """Test create_digest with empty paper list."""
    digest = client.create_digest([])
    
    assert "No papers found" in digest


def test_create_digest_truncates_long_abstract(client):
    """Test that long abstracts are truncated."""
    papers = [
        {
            "title": "Long Abstract Paper",
            "link": "https://example.com",
            "upvotes": 50,
            "abstract": "A" * 300  # Very long abstract
        }
    ]
    
    digest = client.create_digest(papers)
    
    assert "..." in digest
    assert len([line for line in digest.split('\n') if 'A' * 200 in line]) == 0

