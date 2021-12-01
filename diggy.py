#!/usr/bin/env python
# -*- coding: utf-8 -*-
from diggybot.bot import Bot
from diggybot.conversations import *
from diggybot.model import model
import logging

from diggybot.model.entities import Project

VERSION = '0.0.1'

CONVERSATIONS = [
    start,
    notifications
]

# Setup logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    logger.info('Starting diggy-slack-bot v{}'.format(VERSION))

    logger.info('Loading model')
    m = model.Model(logger)

    logger.info('Loading bot')
    bot = Bot(m)
    bot.load_conversations(CONVERSATIONS)
    bot.start()

    logger.info('Bot started')


if __name__ == '__main__':
    main()
