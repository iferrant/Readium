import webapp2
from models.Comment import Comment


class CommentHandler(webapp2.RequestHandler):
    def post(self):
        comment = Comment()
        comment.story_key = self.request.get('story-key')
        comment.author = self.request.get('comment-author')
        comment.text = self.request.get('comment-text')
        comment.put()

        self.redirect("/")
