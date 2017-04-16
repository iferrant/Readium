import webapp2
from webapp2_extras import jinja2


class StoryHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("write_story.html", **{}))
