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


def help(bot, ctxt, client, req, args):
    template_path = os.path.join(os.path.dirname(__file__), 'help.json')
    with open(template_path) as json_data_file:
        template = json.load(json_data_file)
        blocks = template['blocks']
        bot.sendSlackBlocks('#general', blocks, None)


def list_projects(bot, ctxt, client, req, args):
    projects = []
    for row in result:
        projects.append(row[0])
    Project.list_by_id(m.db(), projects, list_projects_response(bot, ctxt, req, res, args))


def list_projects_response(bot, ctxt, client, req, args):
    def list_projects_responseF(result):
        projects = []
        for row in result:
            project = Project(row)
            bot.sendProject('#general', project, None)
    return list_projects_responseF
