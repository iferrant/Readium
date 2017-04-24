from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    lastname = ndb.StringProperty(required=True)
    user_email = ndb.StringProperty(required=True)
    avatar = ndb.BlobProperty(required=False)
    description = ndb.StringProperty(required=False)
    interest = ndb.StringProperty(required=False)
    followers = ndb.StringProperty(repeated=True)
    following = ndb.StringProperty(repeated=True)
    likes = ndb.StringProperty(required=False, repeated=True)
    bookmarks = ndb.StringProperty(required=False, repeated=True)
