#!/usr/bin/python3
import argparse
import json
import os
import re
import sys

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def main():
    load_dotenv()
    args = parse_args()

    with open('emoji_groups.json', 'r') as f:
        groups = json.load(f)

    if args.group in groups:
        client = WebClient(token=get_from_env('SLACK_API_TOKEN'))
        channel, timestamp = parse_link(args.link)
        for emoji in groups[args.group]:
            try:
                client.reactions_add(
                    channel=channel,
                    name=emoji,
                    timestamp=timestamp
                )
            except SlackApiError as e:
                if e.response.data['error'] != 'already_reacted':
                    raise
    else:
        print('Emoji Group not found.')


def get_from_env(key: str):
    try:
        value = os.environ[key]
    except KeyError:
        print(f'No environment variable found for key: [{key}]')
        sys.exit(1)

    return value


def parse_link(link):
    channel = re.findall('[^archives]*(/.*?/)', link)[1][1:-1]
    timestamp = re.findall('([^/]+$)', link)[0][1:]
    timestamp = timestamp[:10] + '.' + timestamp[10:]
    return channel, timestamp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='''
    React to messages on Slack
    ''')

    parser.add_argument('--group', type=str, dest='group',
                        required=True, help='Name of the emoji group to apply')

    # https://twitter.com/SlackAPI/status/911258119099092992
    parser.add_argument('--link', type=str, dest='link',
                        required=True, help='The link to the message you wish to react to')

    return parser.parse_args()


if __name__ == "__main__":
    main()
