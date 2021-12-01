#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

class Model:


    def __init__(self, logger):
        # Logger
        self.log = logger

        # Environment variables
        self.env = EnvOptions()


class EnvOptions:

    def __init__(self):
        self.token = os.environ['TOKEN']
