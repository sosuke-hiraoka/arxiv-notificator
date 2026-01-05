"""
ArXiv Category Client

Fetches category information for papers from arXiv API.
"""

import requests
import xml.etree.ElementTree as ET
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)


class ArxivCategoryClient:
    """Client for fetching paper categories from arXiv API."""
    
    API_URL = "http://export.arxiv.org/api/query"
    
    # Namespace for arXiv API XML response
    NAMESPACES = {
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }
    
    def get_categories(self, arxiv_ids: list[str]) -> dict[str, list[str]]:
        """
        Fetch categories for multiple arXiv papers.
        
        Args:
            arxiv_ids: List of arXiv paper IDs (e.g., ["2501.12345", "2501.67890"])
            
        Returns:
            Dict mapping paper ID to list of categories
        """
        if not arxiv_ids:
            return {}
        
        # Clean IDs (remove version suffix like "v1")
        clean_ids = [self._clean_arxiv_id(aid) for aid in arxiv_ids]
        clean_ids = [aid for aid in clean_ids if aid]
        
        if not clean_ids:
            return {}
        
        try:
            # Build query with id_list parameter
            id_list = ",".join(clean_ids)
            params = {
                "id_list": id_list,
                "max_results": len(clean_ids)
            }
            
            response = requests.get(self.API_URL, params=params, timeout=30)
            response.raise_for_status()
            
            return self._parse_categories(response.text)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch arXiv categories: {e}")
            return {}
    
    def _clean_arxiv_id(self, arxiv_id: str) -> Optional[str]:
        """
        Clean arXiv ID by removing version suffix.
        
        Args:
            arxiv_id: Raw arXiv ID (e.g., "2501.12345v1")
            
        Returns:
            Cleaned ID without version (e.g., "2501.12345")
        """
        if not arxiv_id:
            return None
        
        # Remove version suffix (v1, v2, etc.)
        match = re.match(r'^(\d+\.\d+)', arxiv_id)
        if match:
            return match.group(1)
        
        # Old format: cs/0601001
        match = re.match(r'^([a-z-]+/\d+)', arxiv_id, re.IGNORECASE)
        if match:
            return match.group(1)
        
        return arxiv_id
    
    def _parse_categories(self, xml_content: str) -> dict[str, list[str]]:
        """
        Parse categories from arXiv API XML response.
        
        Args:
            xml_content: XML response string
            
        Returns:
            Dict mapping paper ID to list of categories
        """
        result = {}
        
        try:
            root = ET.fromstring(xml_content)
            
            for entry in root.findall('atom:entry', self.NAMESPACES):
                # Get paper ID from <id> tag
                id_elem = entry.find('atom:id', self.NAMESPACES)
                if id_elem is None or id_elem.text is None:
                    continue
                
                # Extract ID from URL (e.g., "http://arxiv.org/abs/2501.12345v1")
                arxiv_id = self._extract_id_from_url(id_elem.text)
                if not arxiv_id:
                    continue
                
                # Get all categories
                categories = []
                
                # Primary category
                primary = entry.find('arxiv:primary_category', self.NAMESPACES)
                if primary is not None:
                    term = primary.get('term')
                    if term:
                        categories.append(term)
                
                # All categories
                for cat in entry.findall('atom:category', self.NAMESPACES):
                    term = cat.get('term')
                    if term and term not in categories:
                        categories.append(term)
                
                if categories:
                    result[arxiv_id] = categories
            
        except ET.ParseError as e:
            logger.error(f"Failed to parse arXiv XML: {e}")
        
        return result
    
    def _extract_id_from_url(self, url: str) -> Optional[str]:
        """
        Extract arXiv ID from URL.
        
        Args:
            url: arXiv URL (e.g., "http://arxiv.org/abs/2501.12345v1")
            
        Returns:
            Clean arXiv ID without version
        """
        match = re.search(r'/abs/(.+?)(?:v\d+)?$', url)
        if match:
            return self._clean_arxiv_id(match.group(1))
        return None
    
    def matches_categories(
        self,
        paper_categories: list[str],
        target_categories: list[str]
    ) -> bool:
        """
        Check if paper matches any of the target categories.
        
        Args:
            paper_categories: Categories of the paper
            target_categories: Categories to match against
            
        Returns:
            True if paper matches any target category
        """
        paper_set = set(paper_categories)
        target_set = set(target_categories)
        return bool(paper_set & target_set)
