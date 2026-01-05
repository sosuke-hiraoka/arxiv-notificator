"""
Paper Notificator - Main Entry Point

Fetches popular papers from Hugging Face Daily Papers and posts to Slack.
Supports category filtering and history tracking to avoid duplicates.
"""

import os
import sys
import argparse
import logging

from dotenv import load_dotenv

from huggingface_client import HuggingFaceClient
from slack_client import SlackClient
from arxiv_category_client import ArxivCategoryClient
from history_manager import HistoryManager


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Default categories (Agent-related)
DEFAULT_CATEGORIES = "cs.AI,cs.MA,cs.CL"


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch popular papers from Hugging Face and post to Slack"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print digest to stdout instead of posting to Slack"
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=5,
        help="Number of top papers to fetch (default: 5)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Filter papers from past N days (default: 7)"
    )
    parser.add_argument(
        "--categories",
        type=str,
        default=DEFAULT_CATEGORIES,
        help=f"Comma-separated arXiv categories to filter (default: {DEFAULT_CATEGORIES})"
    )
    parser.add_argument(
        "--no-category-filter",
        action="store_true",
        help="Disable category filtering"
    )
    parser.add_argument(
        "--no-history",
        action="store_true",
        help="Disable history tracking (allow duplicates)"
    )
    return parser.parse_args()


def main() -> int:
    """
    Main entry point for Paper Notificator.
    
    Returns:
        0 on success, 1 on error
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Parse CLI arguments
    args = parse_args()
    
    # Validate required environment variables (skip in dry-run mode)
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url and not args.dry_run:
        logger.error("SLACK_WEBHOOK_URL environment variable is required")
        print("Error: SLACK_WEBHOOK_URL environment variable is not set", file=sys.stderr)
        return 1
    
    try:
        # Initialize clients
        hf_client = HuggingFaceClient()
        arxiv_client = ArxivCategoryClient()
        history_manager = HistoryManager()
        
        # Cleanup old history entries
        history_manager.cleanup(days=30)
        
        # Fetch more papers than needed to account for filtering
        fetch_count = args.top_n * 3  # Fetch extra to account for filtering
        logger.info(f"Fetching papers from past {args.days} days...")
        papers = hf_client.fetch_papers(top_n=fetch_count, days=args.days)
        logger.info(f"Fetched {len(papers)} papers from Hugging Face")
        
        # Filter by history (exclude already sent papers)
        if not args.no_history:
            sent_ids = history_manager.get_sent_ids()
            original_count = len(papers)
            papers = [p for p in papers if p.get("arxiv_id") not in sent_ids]
            logger.info(f"After history filter: {len(papers)} papers (excluded {original_count - len(papers)} duplicates)")
        
        # Filter by arXiv categories
        if not args.no_category_filter:
            target_categories = [c.strip() for c in args.categories.split(",")]
            logger.info(f"Filtering by categories: {target_categories}")
            
            # Get arXiv IDs from papers
            arxiv_ids = [p.get("arxiv_id") for p in papers if p.get("arxiv_id")]
            
            if arxiv_ids:
                # Fetch categories for all papers
                paper_categories = arxiv_client.get_categories(arxiv_ids)
                
                # Filter papers by matching categories
                filtered_papers = []
                for paper in papers:
                    arxiv_id = paper.get("arxiv_id")
                    if not arxiv_id:
                        continue  # Skip papers without arXiv ID
                    
                    categories = paper_categories.get(arxiv_id, [])
                    if not categories:
                        # If no category info available, include the paper (fallback)
                        filtered_papers.append(paper)
                    elif arxiv_client.matches_categories(categories, target_categories):
                        filtered_papers.append(paper)
                
                papers = filtered_papers
                logger.info(f"After category filter: {len(papers)} papers")
        
        # Take top N papers
        papers = papers[:args.top_n]
        logger.info(f"Final: {len(papers)} papers to notify")
        
        if not papers:
            logger.info("No new papers matching criteria. Nothing to send.")
            return 0
        
        # Create Slack client and format digest
        slack_client = SlackClient(webhook_url or "")
        digest = slack_client.create_digest(papers)
        
        if args.dry_run:
            # Dry run: print to stdout
            print("\n=== DRY RUN - Slack Message ===\n")
            print(digest)
            print("\n=== END DRY RUN ===\n")
            print(f"\nPapers that would be added to history:")
            for p in papers:
                print(f"  - {p.get('arxiv_id')}: {p.get('title')[:50]}...")
        else:
            # Post to Slack
            logger.info("Posting digest to Slack...")
            slack_client.post_message(digest)
            logger.info("Successfully posted to Slack!")
            
            # Update history with sent papers
            if not args.no_history:
                sent_arxiv_ids = [p.get("arxiv_id") for p in papers if p.get("arxiv_id")]
                history_manager.add(sent_arxiv_ids)
                history_manager.save()
                logger.info(f"Updated history with {len(sent_arxiv_ids)} papers")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
