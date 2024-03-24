import os
import argparse
from notion_client import Client
from notion_client import APIResponseError
# from m_search.notion_blocks import get_all_children_blocks, get_block_type
from m_search.notion_blocks import fetch_and_process_block_hierarchy, fetch_block_details
from m_aux.outputs import prepare_output_folder
from m_aux.pretty_print import pretty_print

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Notion Exporter Application",epilog="NOTE: This program requires the NOTION_TOKEN environment variable to be set.")
    parser.add_argument("-l", "--log_level", help="Set the log level", default="INFO", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument("-o", "--outputs_dir", help="Set the output directory", default="wiki_processed_files")
    
    # Subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='Commands (list or export)')
    
    # List command
    list_parser = subparsers.add_parser('list', help='Generate the hierarchy of the pages in Notion and its children')
    list_parser.add_argument('target', choices=['all', 'page', 'database'], help='Target for the list command')
    list_parser.add_argument('--page-id', '-p', help='ID of the root Notion page',required=True)

    # Export command
    export_parser = subparsers.add_parser('export', help='Prepare the export all the Notion content')
    export_parser.add_argument('target', choices=['all', 'page', 'database'], help='Target for the export command')
    export_parser.add_argument('--page-id', '-p', help='ID of the root Notion page', required=True)
    
    args = parser.parse_args()
    print(args.__dict__)

    # Initialize Notion client with token and set log level
    notion_token = os.environ.get('NOTION_TOKEN')
    notion = Client(auth=notion_token, log_level=args.log_level)
    # Here you would set the log level for the Notion client based on args.log_level
    # Notion client setup code to apply log level goes here (depends on the client's capabilities)

    # Prepare the output folder
    prepare_output_folder(args.outputs_dir)

    # Handle commands
    block_content = fetch_block_details(notion, args.page_id)
    pretty_print(block_content)
    blocks = fetch_and_process_block_hierarchy(notion, args.page_id)
    pretty_print(blocks)
    

if __name__ == "__main__":
    main()
