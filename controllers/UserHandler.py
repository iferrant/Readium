import webapp2
import time
from webapp2_extras import jinja2
from google.appengine.api import users
from models.User import User


class UserProfile(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        current_id = users.get_current_user()
        user = User.query(User.user_email == current_id.nickname())

        if user.count() == 0:
            self.response.write(jinja.render_template("edit_user_profile.html", **{}))
        else:
            values = {
                "user": user
            }
            self.response.write(jinja.render_template("user_profile.html", **values))

    def post(self):
        user_email = users.get_current_user().nickname()
        name = self.request.get('user-name')
        lastname = self.request.get('user-lastname')
        avatar = self.request.get('user-avatar')
        description = self.request.get('user-description')
        interest = self.request.get('user-interest')

        user = User()
        user.user_email = user_email
        user.name = name
        user.lastname = lastname
        if avatar != "":
            user.avatar = avatar
        if description != "":
            user.description = description
        if interest != "":
            user.interest = interest
        user.put()

        time.sleep(2)

        self.redirect("/profile")
