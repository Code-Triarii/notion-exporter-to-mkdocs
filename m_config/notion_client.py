import os

from notion_client import Client

# Initialize the Notion client globally
notion_token = os.environ.get("NOTION_TOKEN")
notion_client = Client(auth=notion_token, log_level="INFO")
notion_request_wait_time_ms = os.environ.get("NOTION_REQUEST_WAIT_TIME", 300)
notion_request_wait_time = int(notion_request_wait_time_ms) / 1000


def set_log_level(log_level):
    global notion_client
    notion_client.log_level = log_level
