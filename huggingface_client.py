"""
HuggingFace Daily Papers Client

Fetches popular papers from Hugging Face Daily Papers API.
"""

import re
import requests
from datetime import datetime, timedelta
from typing import TypedDict, Optional


class Paper(TypedDict):
    """Represents a paper from Hugging Face Daily Papers."""
    title: str
    link: str
    upvotes: int
    abstract: str
    published_at: str
    arxiv_id: Optional[str]


class HuggingFaceClient:
    """Client for fetching papers from Hugging Face Daily Papers API."""
    
    API_URL = "https://huggingface.co/api/daily_papers"
    
    def fetch_papers(self, top_n: int = 5, days: int = 7) -> list[Paper]:
        """
        Fetch top papers from the past week sorted by upvotes.
        
        Args:
            top_n: Number of top papers to return (default: 5)
            days: Filter papers from the past N days (default: 7)
            
        Returns:
            List of Paper objects sorted by upvotes (descending)
            
        Raises:
            requests.RequestException: If API request fails
        """
        response = requests.get(self.API_URL, timeout=30)
        response.raise_for_status()
        
        raw_papers = response.json()
        
        # Calculate date threshold for filtering
        cutoff_date = datetime.now() - timedelta(days=days)
        
        papers: list[Paper] = []
        for item in raw_papers:
            # Parse published date
            published_str = item.get("publishedAt", "")
            try:
                published_dt = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
                if published_dt.replace(tzinfo=None) < cutoff_date:
                    continue
            except (ValueError, TypeError):
                # If date parsing fails, include the paper anyway
                pass
            
            # Extract paper info
            paper_info = item.get("paper", {})
            paper_id = paper_info.get("id", "")  # arXiv ID is in paper.id
            
            paper: Paper = {
                "title": paper_info.get("title", item.get("title", "Untitled")),
                "link": f"https://huggingface.co/papers/{paper_id}",
                "upvotes": paper_info.get("upvotes", 0),
                "abstract": paper_info.get("summary", ""),
                "published_at": published_str,
                "arxiv_id": self.extract_arxiv_id(paper_id)
            }
            papers.append(paper)
        
        # Sort by upvotes descending and return top_n
        papers.sort(key=lambda p: p["upvotes"], reverse=True)
        return papers[:top_n]
    
    def extract_arxiv_id(self, paper_id: str) -> Optional[str]:
        """
        Extract arXiv ID from paper identifier.
        
        Args:
            paper_id: Paper ID from Hugging Face (often same as arXiv ID)
            
        Returns:
            Clean arXiv ID or None if not extractable
        """
        if not paper_id:
            return None
        
        # Match standard arXiv ID format: YYMM.NNNNN or YYMM.NNNNNvN
        match = re.match(r'^(\d{4}\.\d{4,5})(?:v\d+)?$', paper_id)
        if match:
            return match.group(1)
        
        # Match old format: category/YYMMXXX
        match = re.match(r'^([a-z-]+/\d+)(?:v\d+)?$', paper_id, re.IGNORECASE)
        if match:
            return match.group(1)
        
        return None