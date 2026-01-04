"""
Paper Notificator - Main Entry Point

Fetches popular papers from Hugging Face Daily Papers and posts to Slack.
"""

import os
import sys
import argparse
import logging

from dotenv import load_dotenv

from huggingface_client import HuggingFaceClient
from slack_client import SlackClient


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


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
        # Fetch papers from Hugging Face
        logger.info(f"Fetching top {args.top_n} papers from past {args.days} days...")
        hf_client = HuggingFaceClient()
        papers = hf_client.fetch_papers(top_n=args.top_n, days=args.days)
        
        logger.info(f"Fetched {len(papers)} papers")
        
        # Create Slack client and format digest
        slack_client = SlackClient(webhook_url or "")
        digest = slack_client.create_digest(papers)
        
        if args.dry_run:
            # Dry run: print to stdout
            print("\n=== DRY RUN - Slack Message ===\n")
            print(digest)
            print("\n=== END DRY RUN ===\n")
        else:
            # Post to Slack
            logger.info("Posting digest to Slack...")
            slack_client.post_message(digest)
            logger.info("Successfully posted to Slack!")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
