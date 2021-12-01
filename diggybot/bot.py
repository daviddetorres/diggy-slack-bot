#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest

from threading import Event

class Bot:

    def __init__(self, model):
        self.m = model
        self.EVENT_PROCESSORS = {
            "events_api": self.process_events_api,
            "slash_commands": self.process_slash_commands
        }
        self.commands = { }


    def start(self):
        self.m.log.info('Starting slack bot')
        self.client = WebClient(token=self.m.env.token)
        self.socket = SocketModeClient(
            app_token=self.m.env.app_token,
            web_client=self.client
        )
        self.socket.socket_mode_request_listeners.append(self.process())
        self.socket.connect()
        Event().wait()


    def load_conversations(self, conversations):
        for conversation in conversations:
            self.register_conversation(conversation)


    def register_conversation(self, conversation):
        self.m.log.info('Registering conversation: {}'.format(conversation.__name__))

        for command in conversation._commands():
            handle = "/{}".format(command.__name__)
            self.commands[handle] = command


    def process(self):
        def processF(client: SocketModeClient, req: SocketModeRequest):
            req_type = req.type
            processor = self.EVENT_PROCESSORS[req_type]
            processor(client, req)
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)

        return processF


    def process_events_api(self, client: SocketModeClient, req: SocketModeRequest):
        self.m.log.info(req)
        self.sendSlackMessage("#general", "You rock!", None)


    def process_slash_commands(self, client: SocketModeClient, req: SocketModeRequest):
        command = req.payload["command"]
        ctxt = {}
        if command in self.commands:
            self.commands[command](self, ctxt, client, req, None)


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


    def sendSlackBlocks(self, channel, blocks, error_callback):
        try:
            response = self.client.chat_postMessage(channel=channel, blocks=blocks)
            assert response["message"]["blocks"] == blocks
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            # todo error_callback()
            print(f"Got an error: {e.response['error']}")


    def sendProject(self, channel, project, error_callback):
        try:
            text = project.log_string()
            response = self.client.chat_postMessage(channel=channel, text=text)
            assert response["message"]["text"] == text
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            # todo error_callback()
            print(f"Got an error: {e.response['error']}")


    def sendProjectList(self, projects):
        for project in projects:
            bot.sendProject('#general', project, None)


# Start tracker
# register events
# code messages for events

# Conversations
# help command
# create project
# list projects commands
