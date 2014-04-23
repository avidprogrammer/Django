import hashlib
import jinja2
import os
import random
import re
import string
import webapp2

from google.appengine.ext import db

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(autoescape=True,
                               loader=jinja2.FileSystemLoader(templates_dir))

USER_ID = 'user_id'

def make_salt():
  return ''.join(random.choice(string.letters) for i in xrange(5))

def make_hash(name, pwd, salt=None):
  if not salt:
    salt = make_salt()
  h = hashlib.sha256(name + pwd + salt).hexdigest()
  return '%s|%s'%(salt, h)

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
      name_err += "That's not a valid username."
    if not self.valid_pwd(pwd):
      pwd_err += "That's not a valid password."
    elif pwd != verify_pwd:
      pwd_err += "Your passwords dont match"
    if not self.valid_email(email):
      email_err = "That's an invalid email."
    if name_err or pwd_err or email_err:
      self.write({'name_err':name_err, 
                  'pwd_err':pwd_err,
                  'email_err':email_err,
                  'name': name,
                  'email':email})
    else:
      hsh = make_hash(name, pwd) 
      self.response.headers.add_header('Set-cookie', '%s=%s'%(USER_ID, hsh))
      self.redirect('/welcome')

class WelcomePg(webapp2.RequestHandler):
  def get(self):
    user_id = self.request.cookies.get(USER_ID, None)
    if not valid_user_id(user_id):
      self.redirect('/signup')
      return

    self.response.write('<b>Welcome, %s!</b>'%user_id)


app = webapp2.WSGIApplication([
                               ('/', RedirectPg),
                               ('/signup', SignupPg),
                               ('/welcome', WelcomePg),
                              ],
                              debug=True)
