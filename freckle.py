"""Python client for Freckle"""
from cStringIO import StringIO
import datetime
import urllib

import httplib2
import iso8601
import json

class Freckle(object):
    """Class for interacting with the Freckle API"""

    def __init__(self, account, token):
        self.endpoint = "https://%s.letsfreckle.com/api" % account
        self.headers = {"X-FreckleToken":token}
        self.http = httplib2.Http()

    def request(self, url, method="GET", body=""):
        """Make a request to Freckle and return Python objects"""
        resp, content = self.http.request(url, method, body, 
                                          headers=self.headers)
        return json.loads(content)

    def get_entries(self, **kwargs):
        """
        Get time entries from Freckle

        Optional search arguments:

           * people: a list of user ids
           * projects: a list of project ids
           * tags: a list of tag ids and/or names
           * date_to: a `datetime.date` object
           * date_from: a `datetime.date` object
           * billable: a boolean
        """
        search_args = {}
        for search in ('people', 'projects', 'tags'):
            if search in kwargs:
                as_string = ",".join([str(i) for i in kwargs[search]])
                search_args['search[%s]' % search] = as_string
        for search in ('date_to', 'date_from'):
            if search in kwargs:
                date = kwargs[search].strftime("%Y-%m-%d")
                # strip "date_"
                freckle_keyword = 'search[%s]' % search[5:]
                search_args[freckle_keyword] = date
        if "billable" in kwargs:
            if kwargs['billable']:
                val = "true"
            else:
                val = "false"
            search_args['search[billable]'] = val
        query = urllib.urlencode(search_args)
        entry_data = self.request("%s/entries.json?%s" % (self.endpoint, query))
        entries = dict()
        for entry in entry_data:
            entries[entry['entry']['id']] = entry['entry']
        return entries

    def get_users(self):
        """Return users as dict, keyed on ID"""
        users = dict()
        for user in self.request("%s/users.json" % self.endpoint):
            users[user['user']['id']] = user['user']
        return users

    def get_projects(self):
        """Returns projects defined Freckle as a dict, keyed on project id."""
        projects = dict()
        for project in self.request("%s/projects.json" % self.endpoint):
            project_item = project['project']
            project_item['created_at'] = self.datetime_as_python(project_item['created_at'])
            project_item['updated_at'] = self.datetime_as_python(project_item['updated_at'])
            projects[project['project']['id']] = project_item
        return projects
    
    def datetime_as_python(self, val):
        """Convert text to datetime"""
        return iso8601.parse_date(val)

    def integer_as_python(self, val):
        """Convert text to integer"""
        return int(val)
