Usage::

    import freckle
    f = freckle.Freckle(account="apitest",
                        token="lx3gi6pxdjtjn57afp8c2bv1me7g89j")
    f.get_entries(projects=[8475])

This fork uses the JSON output from the Freckle API.

Or a longer example:

    #
    # Collect data from Freckle, and present it in a readable way
    #
    # .freckle-api-token put your API token in a file, or in an ENV var
    #
    import freckle
    import datetime
    import time

    class HelloFreckle(object):
        """Fetches data from API and preps it for script use."""
    
        def __init__(self, apikey):
            super(HelloFreckle, self).__init__()
            self.apikey = apikey
            self.f = freckle.Freckle(account="myaccount", token=apikey)
            self.from_date = datetime.date.fromtimestamp(time.time())
    
        def get_projects(self):
            """Return the Projects defined at myaccount.letsfreckle.com using the API"""
            return self.f.get_projects()
    
        def get_entries(self):
            """Return work item entries using the API"""
            return self.f.get_entries(date_from=self.from_date)
    
        def get_users(self):
            """Return Freckle users"""
            return self.f.get_users()

    xf = HelloFreckle(file('/Users/olle/.freckle-api-token').read().strip())
    projects = xf.get_projects()
    entries = xf.get_entries()
    users = xf.get_users()
    for entry in entries:
        try:
            project = projects[ entries[entry]['project_id'] ]
            try:
                project_name = project['name']
            except KeyError, e:
                project_name = "Bad key"
        except KeyError, e:
            project_name = 'Unknown project'
        print "%s\t%s" % (project_name, entries[entry]['description'])
