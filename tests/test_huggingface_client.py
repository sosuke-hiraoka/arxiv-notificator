"""Tests for HuggingFaceClient."""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

from huggingface_client import HuggingFaceClient, Paper


@pytest.fixture
def client():
    return HuggingFaceClient()


@pytest.fixture
def mock_api_response():
    """Mock API response with sample papers."""
    now = datetime.now()
    return [
        {
            "id": "paper-1",
            "publishedAt": (now - timedelta(days=1)).isoformat() + "Z",
            "paper": {
                "title": "Popular Paper",
                "summary": "This is a popular paper abstract.",
                "upvotes": 100
            }
        },
        {
            "id": "paper-2", 
            "publishedAt": (now - timedelta(days=2)).isoformat() + "Z",
            "paper": {
                "title": "Less Popular Paper",
                "summary": "This is less popular.",
                "upvotes": 50
            }
        },
        {
            "id": "paper-3",
            "publishedAt": (now - timedelta(days=10)).isoformat() + "Z",
            "paper": {
                "title": "Old Paper",
                "summary": "This is an old paper.",
                "upvotes": 200
            }
        }
    ]


def test_fetch_papers_returns_top_n(client, mock_api_response):
    """Test that fetch_papers returns top N papers sorted by upvotes."""
    with patch('huggingface_client.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        papers = client.fetch_papers(top_n=2, days=7)
        
        assert len(papers) == 2
        # Should be sorted by upvotes, old paper filtered out
        assert papers[0]["title"] == "Popular Paper"
        assert papers[0]["upvotes"] == 100
        assert papers[1]["title"] == "Less Popular Paper"


def test_fetch_papers_filters_by_date(client, mock_api_response):
    """Test that papers older than days threshold are filtered out."""
    with patch('huggingface_client.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        papers = client.fetch_papers(top_n=10, days=7)
        
        # Old paper (10 days) should be filtered out
        titles = [p["title"] for p in papers]
        assert "Old Paper" not in titles
        assert len(papers) == 2


def test_fetch_papers_handles_api_error(client):
    """Test that API errors are propagated."""
    with patch('huggingface_client.requests.get') as mock_get:
        mock_get.side_effect = Exception("API Error")
        
        with pytest.raises(Exception):
            client.fetch_papers()


def test_paper_structure(client, mock_api_response):
    """Test that returned papers have correct structure."""
    with patch('huggingface_client.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        papers = client.fetch_papers(top_n=1, days=7)
        
        assert len(papers) == 1
        paper = papers[0]
        assert "title" in paper
        assert "link" in paper
        assert "upvotes" in paper
        assert "abstract" in paper
        assert "published_at" in paper
        assert paper["link"].startswith("https://huggingface.co/papers/")
