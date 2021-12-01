#!/usr/bin/env python
# -*- coding: utf-8 -*-
from diggybot.bot import Bot
from diggybot.model import model
import logging

VERSION = '0.0.1'

CONVERSATIONS = [
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
#    bot.load_conversations(CONVERSATIONS)
    bot.start()

    logger.info('Bot started')

    bot.sendSlackMessage('#general', 'Soy espalda. Digo, I mean, I\'m back.', None)


if __name__ == '__main__':
    main()
