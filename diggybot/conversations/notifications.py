#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..model.entities import *
import os
import json

__name__ = 'Notifications'

def _commands():
    return [
    ]

def _notifications():
    return {
        "new_project": [new_project],
        "new_investment": [new_investment],
        "new_collaborator": [new_collaborator],
        "project_funded": [project_funded]
    }

def new_project(bot, project):
    template_path = os.path.join(os.path.dirname(__file__), 'new_project.json')
    with open(template_path) as json_data_file:
        template = json.load(json_data_file)
        blocks = template['blocks']
        text = template['blocks'][0]['text']['text']
        bot.sendSlackBlocks('#general', text, blocks, None)


def new_investment(bot, invest, user, project):
    template_path = os.path.join(os.path.dirname(__file__), 'new_shovel.json')
    with open(template_path) as json_data_file:
        template = json.load(json_data_file)
        blocks = template['blocks']
        text = template['blocks'][0]['text']['text']
        bot.sendSlackBlocks('#general', text, blocks, None)


def new_collaborator(bot, collaboration, user, project):
    template_path = os.path.join(os.path.dirname(__file__), 'new_contribution.json')
    with open(template_path) as json_data_file:
        template = json.load(json_data_file)
        blocks = template['blocks']
        text = template['blocks'][0]['text']['text']
        bot.sendSlackBlocks('#general', text, blocks, None)


def project_funded(bot, project):
    template_path = os.path.join(os.path.dirname(__file__), 'project_funded.json')
    with open(template_path) as json_data_file:
        template = json.load(json_data_file)
        blocks = template['blocks']
        text = template['blocks'][0]['text']['text']
        bot.sendSlackBlocks('#general', text, blocks, None)

