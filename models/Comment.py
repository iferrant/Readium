from google.appengine.ext import ndb


class Comment(ndb.Model):
    story_key = ndb.StringProperty(required=True)
    author = ndb.StringProperty(required=True)
    text = ndb.StringProperty(required=True)
    date = ndb.DateProperty(required=True, auto_now_add=True)
