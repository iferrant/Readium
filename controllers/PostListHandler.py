import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2
from models.Story import Story
from models.User import User


def create_avatar_dictionary(stories):
    avatars = dict()
    for s in stories:
        user = User.query(User.user_email == s.author)
        user = user.get()
        if user.avatar != "":
            avatars[user.user_email] = user.avatar
        else:
            avatars[user.user_email] = None

    return avatars


class PostListHandler(webapp2.RequestHandler):
    def get(self):
        """
        Get all the stories to create the index feed
        """
        user = users.get_current_user()
        likes = list()
        bookmarks = list()
        if user is not None:
            nickname = user.nickname()
            login_url = users.create_logout_url('/')
            user = User.query(User.user_email == user.nickname())
            user = user.get()
            likes = user.likes
            bookmarks = user.bookmarks
        else:
            nickname = ""
            login_url = users.create_login_url('/')

        jinja = jinja2.get_jinja2(app=self.app)
        stories = Story.query()
        avatars = create_avatar_dictionary(stories)
        values = {
            "stories": stories,
            "nickname": nickname,
            "loginurl": login_url,
            "user": user,
            "likes": likes,
            "bookmarks": bookmarks,
            "avatars": avatars
        }

        self.response.write(jinja.render_template("story_card.html", **values))
