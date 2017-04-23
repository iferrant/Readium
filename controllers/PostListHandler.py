import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2
from models.Story import Story


class PostListHandler(webapp2.RequestHandler):
    def get(self):
        """
        Get all the stories to create the index feed
        """
        user = users.get_current_user()
        if user is not None:
            nickname = user.nickname()
            login_url = users.create_logout_url('/')
        else:
            nickname = ""
            login_url = users.create_login_url('/')

        jinja = jinja2.get_jinja2(app=self.app)
        stories = Story.query()
        values = {
            "stories": stories,
            "nickname": nickname,
            "loginurl": login_url
        }

        self.response.write(jinja.render_template("story_card.html", **values))
