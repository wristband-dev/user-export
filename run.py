#!/usr/bin/env python3
import argparse
import sys
from export_users import get_non_empty_response, generate_csv

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Export users data to CSV.")
    
    # Add arguments
    parser.add_argument('--app_vanity_domain', type=str, help='Application vanity domain')
    parser.add_argument('--app_id', type=str, help='Application ID')
    parser.add_argument('--client_id', type=str, help='Client ID')
    parser.add_argument('--client_secret', type=str, help='Client Secret')
    parser.add_argument('--file_name', type=str, default='users', help='Output CSV file name (default: users)')

    # Parse arguments
    args = parser.parse_args()

    # Check if arguments were provided, otherwise prompt the user
    app_vanity_domain = args.app_vanity_domain or get_non_empty_response("Enter the application vanity domain: ")
    app_id = args.app_id or get_non_empty_response("Enter the application ID: ")
    client_id = args.client_id or get_non_empty_response("Enter the client ID: ")
    client_secret = args.client_secret or get_non_empty_response("Enter the client secret: ")

    # Generate CSV
    generate_csv(app_vanity_domain, app_id, client_id, client_secret, args.file_name)

if __name__ == "__main__":
    main()
