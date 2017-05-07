import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2
from models.Story import Story
from models.User import User


def create_avatar_dictionary(stories):
    """
    Create a dictionary with author email as the key and
    the author's avatar as the value. This dictionary
    will be used to display the avatar on the post card
    :param stories: Stories writen by the user
    :return: Dictionary with K:author email, V:author avatar
    """
    avatars = dict()
    for s in stories:
        user = User.query(User.user_email == s.author)
        user = user.get()
        if user is not None:
            if user.avatar != "":
                avatars[user.user_email] = user.avatar
            else:
                avatars[user.user_email] = None

    return avatars


def create_tags_cloud(stories):
    """
    Create a list with the stories tags
    :param stories: Stories 
    :return: List with stories tags 
    """
    tags = list()
    for s in stories:
        if s.tags:
            print(s.tags)
            tags = tags + s.tags

    return set(filter(None, tags))  # Remove empty tags


def get_tag_stories(stories, tag):
    """
    Retrieve the stories that have the tag "tag"
    :param stories: All the stories
    :param tag: Tag to search
    :return: List of stories with the tag
    """
    result = list()
    for s in stories:
        if s.tags:
            if tag in s.tags:
                result.append(s)
    return result


def search_story(stories, search):
    """
    Retrieve the stories witch title match with "search"
    :param stories: All the stories
    :param search: Word(s) to search in the stories title
    :return: List of stories that contains "search"
    """
    result = list()
    for s in stories:
        if s.title.find(search) != -1 and s not in result:
            result.append(s)
        if s.text.find(search) != -1 and s not in result:
            result.append(s)

    return result


class PostListHandler(webapp2.RequestHandler):
    def get(self):
        """
        Get all the stories to create the index feed
        """
        try:
            tag = self.request.GET['tag']
        except:
            tag = None

        try:
            search = self.request.get('search')
        except:
            search = None

        user = users.get_current_user()
        likes = list()
        bookmarks = list()
        if user is not None:
            nickname = user.nickname()
            login_url = users.create_logout_url('/')
            user = User.query(User.user_email == user.nickname())
            user = user.get()
            if user:
                if user.likes:
                    likes = user.likes
                if user.bookmarks:
                    bookmarks = user.bookmarks
        else:
            nickname = ""
            login_url = users.create_login_url('/')

        jinja = jinja2.get_jinja2(app=self.app)
        stories = Story.query()
        tags = create_tags_cloud(stories)
        if tag:
            # The user is filtering by tag
            stories = get_tag_stories(stories, tag)
        if search:
            # The user searches a story
            stories = search_story(stories, search)
        avatars = create_avatar_dictionary(stories)
        values = {
            "stories": stories,
            "nickname": nickname,
            "loginurl": login_url,
            "user": user,
            "likes": likes,
            "bookmarks": bookmarks,
            "avatars": avatars,
            "cloudtags": tags
        }

        self.response.write(jinja.render_template("story_list.html", **values))
