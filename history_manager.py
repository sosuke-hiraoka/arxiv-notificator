"""
History Manager

Manages sent paper history to prevent duplicate notifications.
"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)


class HistoryManager:
    """Manages history of sent papers to prevent duplicates."""
    
    def __init__(self, filepath: str = "history.json"):
        """
        Initialize HistoryManager.
        
        Args:
            filepath: Path to the history JSON file
        """
        self.filepath = filepath
        self.sent_papers: list[dict] = []
        self.load()
    
    def load(self) -> list[dict]:
        """
        Load history from JSON file.
        
        Returns:
            List of sent paper records
        """
        if not os.path.exists(self.filepath):
            logger.info(f"History file not found, creating new: {self.filepath}")
            self.sent_papers = []
            return self.sent_papers
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.sent_papers = data.get("sent_papers", [])
                logger.info(f"Loaded {len(self.sent_papers)} papers from history")
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load history file: {e}. Starting with empty history.")
            self.sent_papers = []
        
        return self.sent_papers
    
    def is_sent(self, paper_id: str) -> bool:
        """
        Check if a paper has already been sent.
        
        Args:
            paper_id: The paper ID to check
            
        Returns:
            True if paper was already sent, False otherwise
        """
        return any(p.get("id") == paper_id for p in self.sent_papers)
    
    def add(self, paper_ids: list[str]) -> None:
        """
        Add new paper IDs to history.
        
        Args:
            paper_ids: List of paper IDs to add
        """
        today = datetime.now().strftime("%Y-%m-%d")
        for paper_id in paper_ids:
            if not self.is_sent(paper_id):
                self.sent_papers.append({
                    "id": paper_id,
                    "sent_at": today
                })
        logger.info(f"Added {len(paper_ids)} papers to history")
    
    def cleanup(self, days: int = 30) -> int:
        """
        Remove entries older than specified days.
        
        Args:
            days: Number of days to keep entries
            
        Returns:
            Number of entries removed
        """
        cutoff = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff.strftime("%Y-%m-%d")
        
        original_count = len(self.sent_papers)
        self.sent_papers = [
            p for p in self.sent_papers
            if p.get("sent_at", "9999-99-99") >= cutoff_str
        ]
        removed = original_count - len(self.sent_papers)
        
        if removed > 0:
            logger.info(f"Removed {removed} old entries from history")
        
        return removed
    
    def save(self) -> None:
        """Save history to JSON file."""
        data = {"sent_papers": self.sent_papers}
        
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(self.sent_papers)} papers to {self.filepath}")
    
    def get_sent_ids(self) -> set[str]:
        """
        Get set of all sent paper IDs.
        
        Returns:
            Set of paper IDs
        """
        return {p.get("id") for p in self.sent_papers if p.get("id")}
