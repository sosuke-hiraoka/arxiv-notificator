"""
HuggingFace Daily Papers Client

Fetches popular papers from Hugging Face Daily Papers API.
"""

import requests
from datetime import datetime, timedelta
from typing import TypedDict


class Paper(TypedDict):
    """Represents a paper from Hugging Face Daily Papers."""
    title: str
    link: str
    upvotes: int
    abstract: str
    published_at: str


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
            paper: Paper = {
                "title": paper_info.get("title", item.get("title", "Untitled")),
                "link": f"https://huggingface.co/papers/{item.get('id', '')}",
                "upvotes": item.get("paper", {}).get("upvotes", 0),
                "abstract": paper_info.get("summary", ""),
                "published_at": published_str
            }
            papers.append(paper)
        
        # Sort by upvotes descending and return top_n
        papers.sort(key=lambda p: p["upvotes"], reverse=True)
        return papers[:top_n]
