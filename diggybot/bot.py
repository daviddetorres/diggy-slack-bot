#!/usr/bin/env python
# -*- coding: utf-8 -*-
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class Bot:


    def __init__(self, model):
        self.m = model


    def start(self):
        self.m.log.info('Starting slack bot')
        self.client = WebClient(token=self.m.env.token)


    def sendSlackMessage(self, channel, text, error_callback):
        try:
            response = self.client.chat_postMessage(channel=channel, text=text)
            assert response["message"]["text"] == text
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            # todo error_callback()
            print(f"Got an error: {e.response['error']}")

# Start tracker
# register events
# code messages for events

# Conversations
# help command
# create project
# list projects commands
