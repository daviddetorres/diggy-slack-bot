#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sqlalchemy import text
from sqlalchemy import bindparam


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
    def list_ids(db, callback):
        with db.connect() as con:
            statement = """SELECT id, status FROM project"""
            result = con.execute(statement)
        callback(result)


    @staticmethod
    def list_by_id(db, ids, callback):
        params = { 'ids': ids }
        statement = text("""SELECT * FROM project where id IN :ids""")
        statement = statement.bindparams(bindparam('ids', expanding=True))
        with db.connect() as con:
            result = con.execute(statement, params)
        callback(result)
