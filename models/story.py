from google.appengine.ext import ndb


class Story(ndb.Model):
    author = ndb.StringProperty(required=True)
    date = ndb.DateProperty(required=True, auto_now_add=True)
    title = ndb.StringProperty(required=True)
    text = ndb.TextProperty(required=True)
    likes = ndb.IntegerProperty(required=False)
