import webapp2
import time
from models.Comment import Comment


class CommentHandler(webapp2.RequestHandler):
    def post(self):
        """
        Add new comment into a story
        """
        comment = Comment()
        comment.story_key = self.request.get('story-key')
        comment.author = self.request.get('comment-author')
        comment.text = self.request.get('comment-text')
        comment.put()
        time.sleep(1)

        self.redirect("/read_story?id={0}".format(comment.story_key))
