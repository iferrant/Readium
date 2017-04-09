from google.appengine.ext import ndb


class Story(ndb.Model):
    author = ndb.StringProperty(required=True)
    date = ndb.StringProperty(required=False)
    title = ndb.StringProperty(required=True)
    text = ndb.TextProperty(required=True)
