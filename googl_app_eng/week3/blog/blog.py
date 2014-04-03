import jinja2
import os
import webapp2

from google.appengine.ext import db
from models import blogEntry

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(autoescape=True,
                    loader=jinja2.FileSystemLoader(templates_dir))

SUB = 'subject'
CONTENT = 'content'
ERR = 'error'

class Handler(webapp2.RequestHandler):
    def writePage(self, html, **kwargs):
        template = jinja_env.get_template(html)
        self.response.out.write(template.render(**kwargs))

class redirectPage(Handler):
    def get(self):
        self.redirect("/blog") 

class mainPage(Handler):
    def write(self, posts):
        template = jinja_env.get_template("mainPage.html")
        self.writePage(template, posts=posts)

    def get(self):
        posts = db.GqlQuery("select * from blogEntry ORDER BY created DESC " + 
                             "LIMIT 10")
        self.write(posts)

class newPostPage(Handler):
    def write(self, sub="", content="", err=""):
        self.writePage('newPost.html', **{SUB     : sub,
                                          CONTENT : content,
                                          ERR     : err
                                          })

    def get(self):
        self.write()

    def post(self):
        sub = self.request.get(SUB)
        cnt = self.request.get(CONTENT)
        if not sub or not cnt:
            err = 'Please enter a subject and content please :('
            self.write(sub, cnt, err)
        else:
            entry = blogEntry(sub=sub, content=cnt)
            entry.put()
            self.redirect('/blog/%s'%entry.key().id()) 

class entryPage(Handler):
    def write(self, post): 
        self.writePage('entry.html', post=post)

    def get(self, doc_id):
        post = blogEntry.get_by_id(int(doc_id))
        self.write(post)

application = webapp2.WSGIApplication([(r'/', redirectPage),
                                       (r'/blog', mainPage),
                                       (r'/blog/(\d+)', entryPage),
                                       (r'/blog/newpost', newPostPage),
                                      ],
                                      debug=True)

