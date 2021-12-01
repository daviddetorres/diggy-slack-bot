#!/usr/bin/env python
# -*- coding: utf-8 -*-
from entities import *

class Cache:

    def __init__(self, db, projects, invests):
        # Initial data
        self.db = db
        self.projects = []
        self.invests = []

        # Load cache
        self.init_cache()
        self.index_projects(projects)
        self.index_invests(invests)

        # Observers
        self.project_funded_callbacks = []
        self.new_project_callbacks = []
        self.new_invest_callbacks = []
        self.new_collaborator_callbacks = []


    def init_cache(self):
        self.projects_by_id = {}
        self.projects_by_state = {}


    def on_project_funded(self, callback):
        self.project_funded_callbacks.append(callback)


    def on_new_project(self, callback):
        self.new_project_callbacks.append(callback)


    def on_new_invest(self, callback):
        self.new_invest_callbacks.append(callback)


    def on_new_collaborator(self, callback):
        self.new_collaborator_callbacks.append(callback)


    def notify_project_funded(self, project):
        for callback in self.project_funded_callbacks:
            callback(project)


    def notify_new_project(self, project):
        for callback in self.new_project_callbacks:
            callback(project)


    def notify_new_invest(self, invest, user, project):
        for callback in self.new_invest_callbacks:
            callback(invest, user, project)


    def notify_new_collaborator(self, collaboration, user, project):
        for callback in self.new_collaborator_callbacks:
            callback(collaboration, user, project)


    def index_projects(self, projects):
        for project in projects:
            if project in self.projects:
                continue

            self.projects.append(project)

            # Projects by id
            self.projects_by_id[project['id']] = project

            # Projects by state
            if project['state'] not in self.projects_by_state
                self.projects_by_state[project['state']] = []
            self.projects_by_state[project['state']].append(project)


    def index_invests(self, invests):
        for invest in invests:
            if project in self.projects:
                continue

            self.projects.append(project)

            # invests by id
            self.invests_by_id[invest['id']] = invest


    def update_projects(self, new_projects):
        for new in new_projects:
            id = new['id']

            if id in self.projects_by_id:
                old = self.projects_by_id[id]

                # Funded projects
                if old['state'] != new['state'] and new['state'] = 3
                project = Project.find_by_id(self.db, id)
                self.notify_project_funded(project)

            # New projects
            else:
                project = Project.find_by_id(self.db, id)
                self.notify_new_project(project)

            self.projects_by_id.append(new)



    def update_invests(self, new_invests):
