#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..model.entities import *
import os
import json

__name__ = 'Start'

def _commands():
    return [
        help,
        list_projects
    ]


def _notifications():
    return {}


def help(bot, ctxt, client, req, args):
    template_path = os.path.join(os.path.dirname(__file__), 'help.json')
    with open(template_path) as json_data_file:
        template = json.load(json_data_file)
        blocks = template['blocks']
        text = template['blocks'][0]['text']['text']
        bot.sendSlackBlocks('#general', text, blocks, None)


def list_projects(bot, ctxt, client, req, args):
    project_ids = []

    result_project_ids = Project.list_ids(bot.m.db())
    for row in result_project_ids:
        project_ids.append(row[0])

    projects = Project.list_by_id(bot.m.db(), project_ids)

    template = bot.m.template_engine.get_template('project_list.json')
    blocks = template.render(projects=projects,host=bot.m.env.db_host)
    # log the blocks
    # bot.m.log.info(blocks)
    bot.sendSlackBlocks('#general', 'text', blocks, None)
