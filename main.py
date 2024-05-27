# main.py

import argparse
from cli_modules.cli import start, stop
from cli_modules.utils import create_temp_link, ngrok_token

def main():
    parser = argparse.ArgumentParser(description='Create a temporary download link for a file.')
    parser.add_argument('command', choices=['start', 'stop', 'add_file','ngrok_token'], help='Command to execute')
    parser.add_argument('--file', type=str, help='Path to the file')
    parser.add_argument('--token', type=str, help='token of ngrok')
    args = parser.parse_args()

    if args.command == 'start':
        start()
    elif args.command == 'stop':
        stop()
    elif args.command == 'ngrok_token':
        if args.token:
            ngrok_token(args.token)
        else:
            print("Please provide a file path with --token argument.")
    elif args.command == 'add_file':
        if args.file:
            create_temp_link(args.file)
        else:
            print("Please provide a file path with --file argument.")

if __name__ == '__main__':
    main()
