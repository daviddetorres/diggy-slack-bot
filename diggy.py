#!/usr/bin/env python
# -*- coding: utf-8 -*-
from diggybot.bot import Bot
from diggybot.model import model
import logging

from diggybot.model.entities import Project

VERSION = '0.0.1'

CONVERSATIONS = [
]

# Setup logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def cache_projects(result):
    m = model.Model(logger) # Send one as parameter
    projects = []
    for row in result:
        logger.info(row[0])
        projects.append(row[0])
    Project.list_by_id(m.db(), projects, log_projects)


def log_projects(result):
    projects = []
    for row in result:
        project = Project(row)
        projects.append(project)
    send_slack_message(projects)


def send_slack_message(projects):
    bot = Bot(model.Model(logger))  # Send one as parameter
    bot.start()
    #
    for project in projects:
        bot.sendSlackMessage('#general', project.log_string(), None)


def main():

    logger.info('Starting diggy-slack-bot v{}'.format(VERSION))

    logger.info('Loading model')
    m = model.Model(logger)

    logger.info('Loading bot')
    bot = Bot(m)
#    bot.load_conversations(CONVERSATIONS)
    bot.start()

    logger.info('Bot started')

#    Project.list_ids(m.db(), cache_projects)


if __name__ == '__main__':
    main()
