from google.appengine.ext import db

class blogEntry(db.Model):
  sub = db.StringProperty(required=True)
  content = db.TextProperty(required=True, indexed=False)
  created = db.DateTimeProperty(auto_now_add=True)
