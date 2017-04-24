import webapp2
import time
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from models.Story import Story
from models.Comment import Comment
from models.User import User


class StoryHandler(webapp2.RequestHandler):
    def get(self):
        """
        Open the story editor to create a new awesome story
        """
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("write_story.html", **{}))

    def post(self):
        """
        Insert the story created on the datastore
        """
        image = self.request.get('story-image')
        story = Story()
        story.author = users.get_current_user().nickname()
        story.title = self.request.get('story-title')
        story.text = self.request.get('story-text')
        if image:
            story.image = image
        story.put()
        time.sleep(1)

        self.redirect("/")


class ReadStoryHandler(webapp2.RequestHandler):
    def get(self):
        """
        Open the story selected on the read view
        """
        try:
            id = self.request.GET['id']
        except:
            id = None

        time.sleep(2)
        story = ndb.Key(urlsafe=id).get()
        user = users.get_current_user()
        loginurl = users.create_login_url("/")
        comments = Comment.query(id == Comment.story_key)
        read_values = {
            "nickname": user.nickname(),
            "loginurl": loginurl,
            "story": story,
            "user": user,
            "comments": comments
        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("read_story.html", **read_values))


class LikeStoryHandler(webapp2.RequestHandler):
    def post(self):
        """
        When user likes one story, its id is inserted
        on the "likes" array of the user
        If the user isn't logged in, open the login screen
        """
        try:
            story_liked_id = self.request.GET['id']
        except:
            story_liked_id = None

        current_user = users.get_current_user()

        """
        If the user is not logged, open the log page.
        If the user didn't edit his profile, open the edit page.
        Else like or dislike the story.
        """
        if current_user is None:
            self.redirect(users.create_login_url("/"))
        else:
            user = User.query(User.user_email == current_user.nickname())
            user = user.get()
            if user is None:
                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("edit_user_profile.html", **{}))
            else:
                user_key = user.key.urlsafe()

                print(story_liked_id)
                story_liked = ndb.Key(urlsafe=story_liked_id).get()

                if story_liked is not None:
                    print(story_liked.title)
                    if user_key not in story_liked.likes:
                        story_liked.likes.append(user_key)
                        story_liked.put()
                        time.sleep(1)

                        user.likes.append(story_liked_id)
                        user.put()
                        time.sleep(1)
                    else:
                        story_liked.likes.remove(user_key)
                        story_liked.put()
                        time.sleep(1)

                        user.likes.remove(story_liked_id)
                        user.put()
                        time.sleep(1)

                self.redirect("/")

