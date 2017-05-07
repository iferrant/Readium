import webapp2
import time
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from models.Story import Story
from models.Comment import Comment
from models.User import User
#  These three lines are necessary for like/bookmark
#  stories that contains special characters on title
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def create_avatar_dictionary(story, story_id):
    """
    Create a dictionary with author email as the key and
    the author's avatar as the value. This dictionary
    will be used to display the avatar on the story comments
    :param story: Story to be read
    :param story_id: Identifier of the story
    :return: Dictionary with K:author email, V:author avatar
    """
    # Concat 3 lists
    avatars = dict()
    # Retrieve the story author avatar
    if story is not None:
        user = User.query(User.user_email == story.author)
        user = user.get()
        if user is not None:
            if user.avatar != "":
                avatars[user.user_email] = user.avatar
            else:
                avatars[user.user_email] = None
    # Retrieve the comments authors avatars
    if story_id is not None:
        comments = Comment.query(Comment.story_key == story_id)
        for c in comments:
            u = User.query(User.user_email == c.author)
            u = u.get()
            if u is not None:
                if u.avatar != "":
                    avatars[c.author] = u.avatar
                else:
                    avatars[c.author] = None

    return avatars


class WriteStoryHandler(webapp2.RequestHandler):
    def get(self):
        """
        Open the story editor to create a new awesome story
        """
        user = users.get_current_user()
        if user is not None:
            user = user.nickname()

        values = {
            "nickname": user,
            "loginurl": users.create_login_url("/")
        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("write_story.html", **values))

    def post(self):
        """
        Insert the story created on the datastore
        """
        image = self.request.get('story-image')
        tags = self.request.get('story-tags')
        story = Story()
        story.author = users.get_current_user().nickname()
        story.title = self.request.get('story-title')
        story.text = self.request.get('story-text')
        if image:
            story.image = image
        if tags:
            tags = [x.strip() for x in tags.split(',')]  # Split tags
            tags = [x.title() for x in tags]  # Capitalize fist letter
            story.tags = tags
        story.put()
        time.sleep(1)

        self.redirect("/")


class EditStoryHandler(webapp2. RequestHandler):
    """
    Open the story to be edited
    """
    def get(self):
        try:
            id = self.request.GET['id']
        except:
            id = None

        story = ndb.Key(urlsafe=id).get()
        user = users.get_current_user()
        if user is not None:
            user = user.nickname()
        if story is not None:
            values = {
                "story": story,
                "nickname": user,
                "loginurl": users.create_login_url("/")
            }
            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("write_story_edit.html", **values))

        else:
            self.redirect("/")

    def post(self):
        """
        Edit story
        """
        try:
            id = self.request.GET['id']
        except:
            id = None

        story = ndb.Key(urlsafe=id).get()
        if story is not None:
            image = self.request.get('story-image')
            story.title = self.request.get('story-title')
            story.text = self.request.get('story-text')
            if image:
                story.image = image
            story.put()
            time.sleep(1)

        if id is not None:
            self.redirect("/read_story?id={0}".format(id))
        else:
            self.redirect("/")


class RemoveStoryHandler(webapp2.RequestHandler):
    def post(self):
        """
        Remove story
        """
        try:
            id = self.request.GET['id']
        except:
            id = None

        story = ndb.Key(urlsafe=id).get()
        if story is not None:
            if users.get_current_user().nickname() == story.author:
                ndb.Key(urlsafe=id).delete()
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

        story = ndb.Key(urlsafe=id).get()
        user = users.get_current_user()
        if user:
            user = user.nickname()
        else:
            user = None
        loginurl = users.create_login_url("/")
        comments = Comment.query(id == Comment.story_key)
        avatars = create_avatar_dictionary(story, id)
        read_values = {
            "nickname": user,
            "loginurl": loginurl,
            "story": story,
            "user": user,
            "comments": comments,
            "avatars": avatars
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
                self.response.write(jinja.render_template("user_profile_edit.html", **{}))
            else:
                user_key = user.key.urlsafe()

                story_liked = ndb.Key(urlsafe=story_liked_id).get()

                if story_liked is not None:
                    print(story_liked.title)
                    if user_key not in story_liked.likes:
                        story_liked.likes.append(user_key)
                        story_liked.put()

                        user.likes.append(story_liked_id)
                        user.put()
                        time.sleep(1)
                    else:
                        story_liked.likes.remove(user_key)
                        story_liked.put()

                        user.likes.remove(story_liked_id)
                        user.put()
                        time.sleep(1)

                self.redirect("/")

