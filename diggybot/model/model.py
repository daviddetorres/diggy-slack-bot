#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine

class Model:


    def __init__(self, logger):
        # Logger
        self.log = logger

        # Environment variables
        self.env = EnvOptions()

        # Database
        self.db_engine = create_engine(self.env.db_url())


    def db(self):
        return self.db_engine


class EnvOptions:


    def __init__(self):
        self.app_token = os.environ['APP_TOKEN']
        self.token = os.environ['TOKEN']
        self.db_host = os.environ['DB_HOST']
        self.db_port = os.environ['DB_PORT']
        self.db_user = os.environ['DB_USER']
        self.db_pass = os.environ['DB_PASS']
        self.db_database = os.environ['DB_DATABASE']


    def db_url(self):
        return "mysql+pymysql://{}:{}@{}:{}/{}".format(self.db_user, self.db_pass, self.db_host, self.db_port, self.db_database)
