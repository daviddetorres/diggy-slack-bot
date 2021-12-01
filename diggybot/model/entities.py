#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


class Project:

    FIELDS = [
        'id',
        'name',
        'subtitle',
        'description',
        'owner',
        'status'
    ]

    def __init__(self, dict):
        for field in Project.FIELDS:
            setattr(self, field, dict[field])


    def log_string(self):
        return "#{} {} {}".format(self.id, self.name, self.status)

    @staticmethod
    def list_by_id(db, callback):
        with db.connect() as con:
            statement = """SELECT * FROM project"""
#            statement = """SHOW TABLES"""
#            statement = """SHOW COLUMNS FROM project"""
            result = con.execute(statement)
        callback(result)
