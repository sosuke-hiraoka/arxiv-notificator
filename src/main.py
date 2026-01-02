import os
import sys
from dotenv import load_dotenv
from src.arxiv_client import ArxivClient
from src.slack_client import SlackClient

def main():
    """
    Main orchestration function.
    """
    # TODO: Load environment variables using load_dotenv()
    
    # TODO: Retrieve SLACK_WEBHOOK_URL from environment
    # TODO: If webhook url is missing, print error and exit (or raise error)

    # TODO: Define search query (e.g., 'cat:cs.AI') - maybe from env or arg?
    # TODO: Define max_results (e.g., 5)

    # TODO: Initialize ArxivClient
    
    # TODO: Call ArxivClient.fetch_papers(query, max_results)
    # TODO: Log (print) how many papers were fetched

    # TODO: Initialize SlackClient with the webhook url

    # TODO: Call SlackClient.create_digest(papers) to get the formatted message

    # TODO: Check for dry-run flag (sys.argv)
    # TODO: If dry-run, print the digest to stdout and return

    # TODO: Call SlackClient.post_message(digest)
    # TODO: Print success message
    pass

if __name__ == "__main__":
    main()
