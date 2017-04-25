import webapp2
import time
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from models.User import User
from models.Story import Story


def retrieve_like_stories(profile):
    """
    Retrieve stories liked of the user
    :param profile: User
    :return: List of stories
    """
    user_profile = profile.get()
    likes = list()
    if user_profile.likes:
        for l in user_profile.likes:
            likes.append(ndb.Key(urlsafe=l).get())
            time.sleep(1)

    return likes


def retrieve_user_stories(profile):
    """
    Retrieve stories writen of a user
    :param profile: Author 
    :return: List of stories 
    """
    user_profile = profile.get()
    stories = Story.query(Story.author == user_profile.user_email)

    return stories


def retrieve_bookmarks(profile):
    """
    Retrieve bookmarks saved by the user
    :param profile: User
    :return: List of stories
    """
    user_profile = profile.get()
    bookmars = list()
    if user_profile.bookmarks:
        for b in user_profile.bookmarks:
            bookmars.append(ndb.Key(urlsafe=b).get())
            time.sleep(1)

    return bookmars


def retrieve_following(profile):
    """
    Retrieve a list of following users
    :param profile: User 
    :return: List of following users
    """
    user_profile = profile.get()
    following = list()
    if user_profile.following:
        for f in user_profile.following:
            user = User.query(User.user_email == f)
            user = user.get()
            following.append(user)

    return following


def retrieve_followers(profile):
    """
    Retrieve a list of users followers
    :param profile: User 
    :return: List of users followers
    """
    user_profile = profile.get()
    followers = list()
    if user_profile.followers:
        for f in user_profile.followers:
            user = User.query(User.user_email == f)
            user = user.get()
            followers.append(user)

    return followers


class UserProfile(webapp2.RequestHandler):

    def get(self):
        """
        Render the user profile. If the user didn't edit
        his profile yet, open the form to edit the profile.
        If the profile was edited before, open the default
        profile view.
        """
        jinja = jinja2.get_jinja2(app=self.app)

        try:
            profile_email = self.request.GET['user']
        except:
            profile_email = None

        current_id = users.get_current_user()
        if current_id is None:
            self.redirect(users.create_login_url("/"))

        else:
            current_user = current_id.nickname()
            logout_url = users.create_logout_url("/")
            if profile_email == current_user:
                # If the current user is opening his profile
                profile = User.query(User.user_email == current_user)
                if profile.count() == 0:
                    values = {
                        "nickname": current_user,
                        "loginurl": logout_url,
                        "user": None  # necessary because the EditProfileHandler
                    }
                    self.response.write(jinja.render_template("user_profile_edit.html", **values))

                else:
                    stories = retrieve_user_stories(profile)
                    likes = retrieve_like_stories(profile)
                    bookmarks = retrieve_bookmarks(profile)
                    following = retrieve_following(profile)
                    followers = retrieve_followers(profile)
                    values = {
                        "user": profile,
                        "nickname": current_user,
                        "loginurl": logout_url,
                        "following": False,
                        "likes": likes,
                        "stories": stories,
                        "bookmarks": bookmarks,
                        "followinglist": following,
                        "followers": followers
                    }
                    self.response.write(jinja.render_template("user_profile.html", **values))
            else:
                # Open the profile of other user
                profile = User.query(User.user_email == profile_email)
                likes = retrieve_like_stories(profile)
                stories = retrieve_user_stories(profile)
                bookmarks = retrieve_bookmarks(profile)
                following = retrieve_following(profile)
                followers = retrieve_followers(profile)
                u = profile.get()
                is_following = True if current_user in u.followers else False
                values = {
                    "user": profile,
                    "nickname": current_id,
                    "loginurl": logout_url,
                    "following": is_following,
                    "likes": likes,
                    "stories": stories,
                    "bookmarks": bookmarks,
                    "followinglist": following,
                    "followers": followers
                }
                self.response.write(jinja.render_template("user_profile.html", **values))

    def post(self):
        """
        Edit profile of the user
        """
        user_email = users.get_current_user().nickname()
        name = self.request.get('user-name')  # Required
        lastname = self.request.get('user-lastname')  # Required
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

        time.sleep(4)

        self.redirect("/profile?user={0}".format(user_email))


class EditUserHandler(webapp2.RequestHandler):
    def get(self):
        """
        Get the profile of the user to edit.
        The form has as default values the current user values
        """
        jinja = jinja2.get_jinja2(app=self.app)

        try:
            profile_email = self.request.GET['user']
        except:
            profile_email = None

        current_id = users.get_current_user()
        if current_id is None:
            self.redirect(users.create_login_url("/"))
        else:
            user = User.query(User.user_email == profile_email)
            user = user.get()
            values = {
                "nickname": profile_email,
                "loginurl": users.create_logout_url("/"),
                "user": user
            }
            self.response.write(jinja.render_template("user_profile_edit.html", **values))

    def post(self):
        """
        Update the user profile with the new data
        """
        user_email = users.get_current_user().nickname()
        name = self.request.get('user-name')  # Required
        lastname = self.request.get('user-lastname')  # Required
        avatar = self.request.get('user-avatar')
        description = self.request.get('user-description')
        interest = self.request.get('user-interest')

        user = User.query(User.user_email == user_email)
        user = user.get()

        if user is not None:
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
            time.sleep(4)

        self.redirect("/profile?user={0}".format(user_email))


class FollowUserHandler(webapp2.RequestHandler):
    def post(self):
        """
        Add to the following list of the current user the email of
        the user that he's following.
        Add to the followers list of the user that he's following
        the email of the current user.
        If the current user is not logged, open the login window.
        """
        try:
            user_to_follow = self.request.GET['user']
        except:
            user_to_follow = None

        current_user = users.get_current_user()
        c_user = User.query(User.user_email == current_user.nickname())
        f_user = User.query(User.user_email == user_to_follow)

        if c_user.get() is None:
            self.redirect("/profile?user={0}".format(current_user.nickname()))
        else:
            user = c_user.get()
            follow_user = f_user.get()

            user.following.append(follow_user.user_email)
            user.put()
            time.sleep(1)

            follow_user.followers.append(user.user_email)
            follow_user.put()
            time.sleep(1)

            print(user.following)
            print(follow_user.followers)
            self.redirect("/profile?user={0}".format(user_to_follow))


class UnFollowHandler(webapp2.RequestHandler):
    def post(self):
        """
        Remove from the following list of the current user the email of
        the user that he's unfollowing.
        Remove from the followers list of the user that he's unfollowing
        the email of the current user.
        """
        try:
            user_to_unfollow = self.request.GET['user']
        except:
            user_to_unfollow = None

        current_user = users.get_current_user()
        c_user = User.query(User.user_email == current_user.nickname())
        u_user = User.query(User.user_email == user_to_unfollow)

        user = c_user.get()
        unfollow_user = u_user.get()
        if user.user_email in unfollow_user.followers:
            unfollow_user.followers.remove(user.user_email)
            unfollow_user.put()
            time.sleep(1)

        if unfollow_user.user_email in user.following:
            user.following.remove(unfollow_user.user_email)
            user.put()
            time.sleep(1)

        self.redirect("/profile?user={0}".format(user_to_unfollow))


class BookmarkStoryHandler(webapp2.RequestHandler):
    def post(self):
        """
        Save the story id on the bookmarks list of the user
        """
        try:
            story_id = self.request.GET['id']
        except:
            story_id = None

        current_user = users.get_current_user()
        c_user = User.query(User.user_email == current_user.nickname())
        user = c_user.get()
        if story_id in user.bookmarks:
            user.bookmarks.remove(story_id)
        else:
            user.bookmarks.append(story_id)
        user.put()
        time.sleep(1)

        self.redirect("/")
