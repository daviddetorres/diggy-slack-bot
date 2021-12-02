#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import text
from sqlalchemy import bindparam


class Project:

    FIELDS = [
        'id',
        'name',
        'subtitle',
        'description',
        'owner',
        'status',
        'mincost',
        'maxcost',
        'amount',
        'num_investors',
        'image'
    ]

    def __init__(self, dict):
        for field in Project.FIELDS:
            setattr(self, field, dict[field])


    def log_string(self):
        return "#{} {} {}".format(self.id, self.name, self.status)

    @staticmethod
    def list_ids(db):
        with db.connect() as con:
            statement = """SELECT id, status FROM project WHERE status = 3"""
            return con.execute(statement)


    @staticmethod
    def list_by_id(db, ids):
        result_list = []

        params = { 'ids': ids }
        statement = text("""SELECT * FROM project where id IN :ids""")
        statement = statement.bindparams(bindparam('ids', expanding=True))

        with db.connect() as con:
            result = con.execute(statement, params)

            for row in result:
                result_list.append( Project(row) )

        return result_list


    @staticmethod
    def find_by_id(db, id):
        result_object = []

        params = { 'id': id }
        statement = text("""SELECT * FROM project where id = :id""")
        statement = statement.bindparams(bindparam('id'))

        with db.connect() as con:
            result = con.execute(statement, params)

            result_object = Project(result.fetchone())

        return result_object


class Need:

    FIELDS = [
        'project_id',
        'need_id',
        'name',
        'subtitle',
        'need',
        'need_description'
    ]

    def __init__(self, dict):
        for field in Need.FIELDS:
            setattr(self, field, dict[field])

    def log_string(self):
        return "#{} {} {}".format(self.id, self.name, self.status)

    @staticmethod
    def list_ids(db):
        with db.connect() as con:
            statement = """SELECT id, status FROM project WHERE status = 3 and (SELECT COUNT(*) FROM support WHERE support.project = project.id) > 0;"""
            return con.execute(statement)

    @staticmethod
    def list_by_id(db,ids):
        result_list = []

        params = { 'ids': ids }
        
        statement = text("""SELECT 
                        p.id as project_id,
                        s.id as need_id,
                        p.name as name, 
                        p.subtitle as subtitle,
                        s.support as need,
                        s.description as need_description
                        FROM project as p, support as s
                        WHERE 
                        p.id IN :ids
                        AND p.status = 3
                        AND p.id = s.project;""")

        statement = statement.bindparams(bindparam('ids', expanding=True))
        with db.connect() as con:
            result = con.execute(statement, params)
            for row in result:
                result_list.append( Need(row) )

        return result_list



class Invest:

    FIELDS = [
        'id',
        'user',
        'project',
        'amount',
        'currency'
    ]

    def __init__(self, dict):
        for field in Invest.FIELDS:
            setattr(self, field, dict[field])


    def log_string(self):
        return "#{} by {} on {} - {}{}".format(self.id, self.user, self.project, self.ammount, self.currency)

    @staticmethod
    def list_ids(db):
        with db.connect() as con:
            statement = """SELECT id FROM invest"""
            return con.execute(statement)


    @staticmethod
    def list_by_id(db, ids):
        result_list = []

        params = { 'ids': ids }
        statement = text("""SELECT * FROM invest where id IN :ids""")
        statement = statement.bindparams(bindparam('ids', expanding=True))

        with db.connect() as con:
            result = con.execute(statement, params)

            for row in result:
                result_list.append( Invest(row) )

        return result_list


    @staticmethod
    def find_by_id(db, id):
        result_object = []

        params = { 'id': id }
        statement = text("""SELECT * FROM invest where id = :id""")
        statement = statement.bindparams(bindparam('id'))

        with db.connect() as con:
            result = con.execute(statement, params)

            result_object = Invest(result.fetchone())

        return result_object

