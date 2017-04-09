import webapp2
from webapp2_extras import jinja2
from models.story import Story


class MainHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("base.html", **{}))


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("login.html", **{}))


class CardHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        author = "ivan"
        date = "10.10.10"
        title = self.request.get("story-title")
        text = self.request.get("story-text")

        stories = Story.query()
        story = Story(author=author, date=date, title=title, text=text)
        story.put()

        values = {
            "stories": stories
        }

        self.response.write(jinja.render_template("post_card.html", **values))


class StoryHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("write_story.html", **{}))

