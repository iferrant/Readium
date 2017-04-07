import webapp2
from webapp2_extras import jinja2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("base.html", **{}))


class LoginHandler(webapp2.RedirectHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("login.html", **{}))


class CardHandler(webapp2.RedirectHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("post_card.html", **{}))
