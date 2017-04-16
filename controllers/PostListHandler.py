import webapp2
from webapp2_extras import jinja2
from models.story import Story


class PostListHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        stories = Story.query()
        values = {
            "stories": stories
        }
        self.response.write(jinja.render_template("post_card.html", **values))

    def post(self):
        story = Story()
        story.author = "ivan"
        story.title = self.request.get('story-title')
        story.text = self.request.get('story-text')
        story.put()

        self.redirect("/")
