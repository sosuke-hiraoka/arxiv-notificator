"""Tests for HistoryManager."""

import pytest
import json
import os
import tempfile
from datetime import datetime, timedelta

from history_manager import HistoryManager


@pytest.fixture
def temp_history_file():
    """Create a temporary history file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"sent_papers": []}, f)
        filepath = f.name
    yield filepath
    if os.path.exists(filepath):
        os.unlink(filepath)


def test_load_creates_empty_if_not_exists():
    """Test that load creates empty history if file doesn't exist."""
    manager = HistoryManager("/nonexistent/path/history.json")
    assert manager.sent_papers == []


def test_load_existing_file(temp_history_file):
    """Test loading existing history file."""
    # Prepare test data
    test_data = {
        "sent_papers": [
            {"id": "2501.12345", "sent_at": "2026-01-05"},
            {"id": "2501.67890", "sent_at": "2026-01-04"}
        ]
    }
    with open(temp_history_file, 'w') as f:
        json.dump(test_data, f)
    
    manager = HistoryManager(temp_history_file)
    assert len(manager.sent_papers) == 2


def test_is_sent(temp_history_file):
    """Test is_sent check."""
    test_data = {
        "sent_papers": [{"id": "2501.12345", "sent_at": "2026-01-05"}]
    }
    with open(temp_history_file, 'w') as f:
        json.dump(test_data, f)
    
    manager = HistoryManager(temp_history_file)
    assert manager.is_sent("2501.12345") is True
    assert manager.is_sent("2501.99999") is False


def test_add_papers(temp_history_file):
    """Test adding papers to history."""
    manager = HistoryManager(temp_history_file)
    manager.add(["2501.11111", "2501.22222"])
    
    assert manager.is_sent("2501.11111") is True
    assert manager.is_sent("2501.22222") is True
    assert len(manager.sent_papers) == 2


def test_add_skips_duplicates(temp_history_file):
    """Test that add skips already sent papers."""
    manager = HistoryManager(temp_history_file)
    manager.add(["2501.11111"])
    manager.add(["2501.11111", "2501.22222"])
    
    assert len(manager.sent_papers) == 2


def test_save(temp_history_file):
    """Test saving history to file."""
    manager = HistoryManager(temp_history_file)
    manager.add(["2501.12345"])
    manager.save()
    
    # Load and verify
    with open(temp_history_file, 'r') as f:
        data = json.load(f)
    
    assert len(data["sent_papers"]) == 1
    assert data["sent_papers"][0]["id"] == "2501.12345"


def test_cleanup_old_entries(temp_history_file):
    """Test cleanup removes old entries."""
    old_date = (datetime.now() - timedelta(days=35)).strftime("%Y-%m-%d")
    recent_date = datetime.now().strftime("%Y-%m-%d")
    
    test_data = {
        "sent_papers": [
            {"id": "old_paper", "sent_at": old_date},
            {"id": "recent_paper", "sent_at": recent_date}
        ]
    }
    with open(temp_history_file, 'w') as f:
        json.dump(test_data, f)
    
    manager = HistoryManager(temp_history_file)
    removed = manager.cleanup(days=30)
    
    assert removed == 1
    assert manager.is_sent("old_paper") is False
    assert manager.is_sent("recent_paper") is True


def test_get_sent_ids(temp_history_file):
    """Test get_sent_ids returns set of IDs."""
    test_data = {
        "sent_papers": [
            {"id": "2501.12345", "sent_at": "2026-01-05"},
            {"id": "2501.67890", "sent_at": "2026-01-04"}
        ]
    }
    with open(temp_history_file, 'w') as f:
        json.dump(test_data, f)
    
    manager = HistoryManager(temp_history_file)
    ids = manager.get_sent_ids()
    
    assert ids == {"2501.12345", "2501.67890"}
