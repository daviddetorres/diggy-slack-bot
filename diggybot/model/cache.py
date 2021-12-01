#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .entities import *
import time, threading

CACHE_UPDATE_SECONDS = 10

class Cache:

    def __init__(self, model, projects, invests):
        # Initial data
        self.m = model
        self.db = model.db()
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

        # Update cache
        threading.Timer(CACHE_UPDATE_SECONDS, self.refresh_cache).start()

    def init_cache(self):
        self.projects_by_id = {}
        self.projects_by_status = {}
        self.invests_by_id = {}


    def refresh_cache(self):
        self.m.log.info("Refreshing cache")
        projects = Project.list_ids(self.db)
        invests = Invest.list_ids(self.db)

        self.index_projects(projects)
        self.index_invests(projects)

        threading.Timer(CACHE_UPDATE_SECONDS, self.refresh_cache).start()


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

            # Projects by status
            status = project['status']
            if status not in self.projects_by_status:
                self.projects_by_status[status] = []
            if project in self.projects_by_status[status]:
                self.projects_by_status[status].remote(project)
            self.projects_by_status[status].append(project)


    def index_invests(self, invests):
        for invest in invests:
            if invest in self.invests:
                continue

            self.invests.append(invest)

            # invests by id
            self.invests_by_id[invest['id']] = invest


    def update_projects(self, new_projects):
        projects_to_index = []

        for new in new_projects:
            id = new['id']

            if id in self.projects_by_id:
                old = self.projects_by_id[id]

                # Funded projects
                if old['status'] != new['status'] and new['status'] == 3:
                    project = Project.find_by_id(self.db, id)
                    projects_to_index.append(project)
                    self.notify_project_funded(project)

            # New projects
            else:
                project = Project.find_by_id(self.db, id)
                projects_to_index.append(project)
                self.notify_new_project(project)

        self.index_projects(projects_to_index)



    def update_invests(self, new_invests):
        invests_to_index = []

        for new in new_invests:
            id = new['id']

            # New invests
            if id not in self.invests_by_id:
                invest = Invest.find_by_id(self.db, id)
                invests_to_index.append(invest)
                user = None # TODO
                project = None # TODO
                self.notify_new_invest(invest, user, project)

        self.index_invests(invests_to_index)
