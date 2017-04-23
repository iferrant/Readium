from google.appengine.ext import ndb


class Story(ndb.Model):
    image = ndb.BlobProperty(required=False)
    author = ndb.StringProperty(required=True)
    date = ndb.DateProperty(required=True, auto_now_add=True)
    title = ndb.StringProperty(required=True)
    text = ndb.TextProperty(required=True)
    likes = ndb.StringProperty(required=False, repeated=True)
