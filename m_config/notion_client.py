import os

from notion_client import Client

# Initialize the Notion client globally
notion_token = os.environ.get("NOTION_TOKEN")
notion_client = Client(auth=notion_token, log_level="INFO")


def set_log_level(log_level):
    global notion_client
    notion_client.log_level = log_level
