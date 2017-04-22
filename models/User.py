from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    lastname = ndb.StringProperty(required=True)
    user_email = ndb.StringProperty(required=True)
    avatar = ndb.BlobProperty(required=False)
    description = ndb.StringProperty(required=False)
    interest = ndb.StringProperty(required=False)
    followers = ndb.IntegerProperty(default=0)
    following = ndb.IntegerProperty(default=0)

