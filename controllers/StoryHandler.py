import webapp2
from webapp2_extras import jinja2
from google.appengine.ext import ndb


class StoryHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("write_story.html", **{}))


class ReadStoryHandler(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['id']

        except:
            id = None

        story = ndb.Key(urlsafe=id).get()
        read_values = {
            "story": story
        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("read_story.html", **read_values))
