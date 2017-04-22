import webapp2
import time
from webapp2_extras import jinja2
from google.appengine.api import users
from models.User import User


class UserProfile(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)

        try:
            user_email = self.request.GET['user']
        except:
            user_email = None

        current_id = users.get_current_user().nickname()

        if user_email == current_id:
            user = User.query(User.user_email == current_id)
            if user.count() == 0:
                self.response.write(jinja.render_template("edit_user_profile.html", **{}))
            else:
                values = {
                    "user": user,
                }
                self.response.write(jinja.render_template("user_profile.html", **values))
        else:
            user = User.query(User.user_email == user_email)
            values = {
                "user": user,
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
        user.followers = list()
        user.following = list()
        user.put()

        time.sleep(1)

        self.redirect("/profile?user={0}".format(user_email))


class FollowUserHandler(webapp2.RequestHandler):
    def get(self):
        pass

    def post(self):
        try:
            user_to_follow = self.request.GET['user']
        except:
            user_to_follow = None

        current_user = users.get_current_user()
        c_user = User.query(User.user_email == current_user.nickname())
        f_user = User.query(User.user_email == user_to_follow)

        if c_user.count == 0:
            self.redirect(users.create_login_url("/"))
        else:
            user = c_user.get()
            follow_user = f_user.get()
            user.followers.append('{0}'.format(follow_user.user_email))
            user.put()
            time.sleep(1)
            self.redirect("/profile?user={0}".format(user_to_follow))
