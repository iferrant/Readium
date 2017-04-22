import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users, images
from google.appengine.ext import ndb
from models.Story import Story
from models.Comment import Comment


class StoryHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("write_story.html", **{}))

    def post(self):
        image = self.request.get('story-image')
        story = Story()
        story.author = users.get_current_user().nickname()
        story.title = self.request.get('story-title')
        story.text = self.request.get('story-text')
        if image:
            story.image = image
        story.put()

        self.redirect("/")


class ReadStoryHandler(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['id']
        except:
            id = None

        story = ndb.Key(urlsafe=id).get()
        user = users.get_current_user()
        comments = Comment.query(id == Comment.story_key)
        read_values = {
            "story": story,
            "user": user,
            "comments": comments
        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("read_story.html", **read_values))
