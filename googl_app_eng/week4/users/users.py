import hashlib
import jinja2
import os
import random
import re
import string
import webapp2

from google.appengine.ext import db
from models import UserInfo

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(autoescape=True,
                               loader=jinja2.FileSystemLoader(templates_dir))

USER_ID = 'user_id'

class Handler(webapp2.RequestHandler):
    def writePage(self, template, **kwargs):
      html = jinja_env.get_template(template)
      self.response.out.write(html.render(**kwargs))

class RedirectPg(Handler):
  def get(self):
    self.redirect('/signup')

class SignupPg(Handler):
  USER_RE = re.compile(r"^[a-zA-z0-9_-]{3,20}$")
  PWD_RE = re.compile(r"^.{3,20}$")
  EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

  def write(self, kwargs={}):
    self.writePage('signup.html', **kwargs)

  def valid_name(self, name):
    return self.USER_RE.match(name)

  def valid_pwd(self, pwd):
    return self.PWD_RE.match(pwd) 

  def valid_email(self, email):
    if not email:
      return True
    return self.EMAIL_RE.match(email) 
  
  def make_salt(self):
    return ''.join(random.choice(string.letters) for i in xrange(5))

  def make_hash(self, name, pwd, salt=None):
    if not salt:
      salt = self.make_salt()
    h = hashlib.sha256(name + pwd + salt).hexdigest()
    return '%s|%s'%(salt, h)

  def get_user_by_name(self, name):
    user = db.GqlQuery("SELECT * FROM UserInfo WHERE name = '%s'"%name).get()
    return user

  def is_valid_login(self, name, pwd, user):
    salt = user.hash_str.split('|')[0] 
    hsh = self.make_hash(name, pwd, salt)
    return hsh == user.hash_str

  def create_user(self, name, pwd):
      hsh = self.make_hash(name, pwd)
      new_user = UserInfo(name=name, hash_str=hsh)
      new_user.put()
      return new_user 

  def login(self, user):
      self.response.headers.add_header('Set-cookie', '%s=%s'%(USER_ID, 
                                                          str(user.hash_str)))
      self.redirect('/welcome')
  
  def logout(self):
      self.response.headers.add_header('Set-cookie', '%s=; Path=/'%USER_ID)
      self.redirect('/signup')

  def get(self):
    self.write()

  def post(self):
    name_err = ""
    pwd_err = ""
    email_err = ""

    name = self.request.get('username')
    pwd = self.request.get('password')
    verify_pwd = self.request.get('verify')
    email = self.request.get('email')
    
    if not self.valid_name(name): 
      name_err = "That's not a valid username."
    elif self.get_user_by_name(name):
      name_err = "User already exists!"
    if not self.valid_pwd(pwd):
      pwd_err = "That's not a valid password."
    elif pwd != verify_pwd:
      pwd_err = "Your passwords dont match"
    if not self.valid_email(email):
      email_err = "That's an invalid email."
    if name_err or pwd_err or email_err:
      self.write({'name_err':name_err, 
                  'pwd_err':pwd_err,
                  'email_err':email_err,
                  'name': name,
                  'email':email})
    else:
      user = self.create_user(name, pwd)
      self.login(user)

class WelcomePg(webapp2.RequestHandler):
  def get(self):
    user_hsh = self.request.cookies.get(USER_ID, None)
    user = db.GqlQuery("Select * from UserInfo WHERE hash_str='%s'"%user_hsh).get()
    if not user:
      self.redirect('/signup')
      return

    self.response.write('<b>Welcome, %s!</b>'%user.name)

class LoginPg(SignupPg):
  def write(self, kwargs={}):
    self.writePage('login.html', **kwargs)

  def post(self):
    name = self.request.get('username')
    pwd = self.request.get('password')
    user = self.get_user_by_name(name) 
    if user and self.is_valid_login(name, pwd, user):
      self.login(user)
    else:
      self.write({'login_err':'Invalid Login'})

class LogoutPg(SignupPg):
  def get(self):
    self.logout()

app = webapp2.WSGIApplication([
                               ('/', RedirectPg),
                               ('/signup', SignupPg),
                               ('/welcome', WelcomePg),
                               ('/login', LoginPg),
                               ('/logout', LogoutPg),
                              ],
                              debug=True)
