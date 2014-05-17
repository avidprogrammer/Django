from google.appengine.ext import db

class UserInfo(db.Model):
  name = db.StringProperty(required=True)
  hash_str = db.StringProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)
