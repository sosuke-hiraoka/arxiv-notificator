"""Tests for ArxivCategoryClient."""

import pytest
from unittest.mock import MagicMock, patch

from arxiv_category_client import ArxivCategoryClient


@pytest.fixture
def client():
    return ArxivCategoryClient()


@pytest.fixture
def mock_arxiv_response():
    """Mock arXiv API XML response."""
    return '''<?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
        <entry>
            <id>http://arxiv.org/abs/2501.12345v1</id>
            <arxiv:primary_category term="cs.AI"/>
            <category term="cs.AI"/>
            <category term="cs.CL"/>
        </entry>
        <entry>
            <id>http://arxiv.org/abs/2501.67890v2</id>
            <arxiv:primary_category term="cs.CV"/>
            <category term="cs.CV"/>
        </entry>
    </feed>'''


def test_get_categories_success(client, mock_arxiv_response):
    """Test successful category fetching."""
    with patch('arxiv_category_client.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.text = mock_arxiv_response
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        result = client.get_categories(["2501.12345", "2501.67890"])
        
        assert "2501.12345" in result
        assert "cs.AI" in result["2501.12345"]
        assert "cs.CL" in result["2501.12345"]
        assert "2501.67890" in result
        assert "cs.CV" in result["2501.67890"]


def test_get_categories_empty_list(client):
    """Test with empty ID list."""
    result = client.get_categories([])
    assert result == {}


def test_get_categories_api_error(client):
    """Test handling of API errors."""
    with patch('arxiv_category_client.requests.get') as mock_get:
        import requests
        mock_get.side_effect = requests.RequestException("API Error")
        
        result = client.get_categories(["2501.12345"])
        assert result == {}


def test_clean_arxiv_id(client):
    """Test arXiv ID cleaning."""
    assert client._clean_arxiv_id("2501.12345v1") == "2501.12345"
    assert client._clean_arxiv_id("2501.12345v2") == "2501.12345"
    assert client._clean_arxiv_id("2501.12345") == "2501.12345"
    assert client._clean_arxiv_id("cs/0601001v1") == "cs/0601001"


def test_matches_categories(client):
    """Test category matching."""
    assert client.matches_categories(["cs.AI", "cs.CL"], ["cs.AI", "cs.MA"])
    assert client.matches_categories(["cs.AI"], ["cs.AI"])
    assert not client.matches_categories(["cs.CV"], ["cs.AI", "cs.MA"])


def test_extract_id_from_url(client):
    """Test ID extraction from arXiv URL."""
    assert client._extract_id_from_url("http://arxiv.org/abs/2501.12345v1") == "2501.12345"
    assert client._extract_id_from_url("http://arxiv.org/abs/2501.67890") == "2501.67890"
