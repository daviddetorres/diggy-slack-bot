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

        cache = self.m.cache
        notifications = conversation._notifications()
        for notification_type in notifications:
            callbacks = notifications[notification_type]
            for callback in callbacks:
                if notification_type == "new_project":
                    cache.on_new_project(self.create_new_project_callback(callback))
                elif notification_type == "new_investment":
                    cache.on_new_invest(self.create_new_invest_callback(callback))
                elif notification_type == "new_collaborator":
                    cache.on_new_collaborator(self.create_new_collaborator_callback(callback))
                elif notification_type == "project_funded":
                    cache.on_project_funded(self.create_project_funded_callback(callback))


    def create_new_project_callback(self, callback):
        def notification_callback(project):
            callback(self, project)
        return notification_callback


    def create_new_invest_callback(self, callback):
        def notification_callback(invest, user, project):
            callback(self, invest, user, project)
        return notification_callback


    def create_new_collaborator_callback(self, callback):
        def notification_callback(collaboration, user, project):
            callback(self, collaboration, user, project)
        return notification_callback


    def create_project_funded_callback(self, callback):
        def notification_callback(project):
            callback(self, project)
        return notification_callback


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
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            # todo error_callback()
            print(f"Got an error: {e.response['error']}")


    def sendSlackBlocks(self, channel, text, blocks, error_callback):
        try:
            response = self.client.chat_postMessage(channel=channel, text=text, blocks=blocks)
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
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            # todo error_callback()
            print(f"Got an error: {e.response['error']}")


    def sendProjectList(self, channel, projects):
        for project in projects:
            self.sendProject(channel, project, None)

# Conversations
# create project
# list projects commands
