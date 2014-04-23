from google.appengine.ext import db

class UserInfo(db.model):
  name = db.StringProperty(required=True)
  hash_str = db.StringProperty(required=True)

