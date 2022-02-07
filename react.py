#!/usr/bin/python3
from slack_sdk import WebClient
import os
import sys
import argparse
from dotenv import load_dotenv

# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)


def main():

    load_dotenv()
    args = parse_args()
    print(getFromEnv('SLACK_API_TOKEN'))
    print(args.group)
    # client = WebClient()
    # api_response = client.api_test()


def getFromEnv(key: str):
    try:
        value = os.environ[key]
    except KeyError:
        print(f'No environment variable found for key: [{key}]')
        sys.exit(1)
    
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='''
    TODO
    ''')

    parser.add_argument('--group', type=str, dest='group',
                        required=True, help='Name of the emoji group to apply')

    return parser.parse_args()


if __name__ == "__main__":
    main()
