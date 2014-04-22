import re
import webapp2
from cgi import escape as cgi_esc

USER_RE = re.compile(r"^[a-zA-z0-9_-]{3,20}$")
PWD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

form_html = """
<h2> Enter text to encode with ROT13</h2>
<form method="post">
    <textarea tows="4" cols="50" name="text" />%(content)s</textarea>
    <br>
    <input type="submit" value="Submit">
</form>
"""

signup_html = """
<head>
<style>
  .error {
    color:red;
  }
</style>
</head>
<h2> Signup </h2>
<form method="post">
  <table>
    <tr>
      <td> Username </td>
      <td> <Input type="text" name="username" value=%(name)s> </td>
      <td class="error"> %(name_err)s </td>
    </tr>
    <tr>
      <td> Password </td>
      <td> <Input type="password" name="password"> </td>
      <td class="error"> %(pwd_err)s </td>
    </tr>
    <tr>
      <td> Verify Password</td>
      <td> <Input type="password" name="verify"> </td>
    </tr>
    <tr>
      <td> Email (Optional) </td>
      <td> <Input type="text" name="email" value=%(email)s> </td>
      <td class="error"> %(email_err)s </td>
    </tr>
 </table>
 <input type="submit" value="Submit">
</form>
"""

LOOKUP = {}
ASCII_A = 65
ASCII_Z = 90
ASCII_a = 97
ASCII_z = 122
UPPER_ALPHA = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
LOWER_ALPHA = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()

def cipher(char):
  global LOOKUP

  if char in LOOKUP:
     return LOOKUP[char]
  if char.isupper():
      nchar = UPPER_ALPHA[(UPPER_ALPHA.index(char) + 13)%26]
  else:
      nchar = LOWER_ALPHA[(LOWER_ALPHA.index(char) + 13)%26]
  LOOKUP[char] = nchar
  return nchar

def text_manip(ip_txt):
  op_txt = ''
  for c in ip_txt:
      if not c.isalpha():
          op_txt += c
      else:
          op_txt += cipher(c) 
  return op_txt

class ROT13Page(webapp2.RequestHandler):

  def write_html(self, content=""):
      self.response.write(form_html%{'content' : cgi_esc(content, quote=True)})

  def get(self):
      self.write_html()

  def post(self):
      text = self.request.get('text')
      self.write_html(text_manip(text))


def valid_name(name):
  return USER_RE.match(name)

def valid_pwd(pwd):
  return PWD_RE.match(pwd) 

def valid_email(email):
  if not email:
    return True
  return EMAIL_RE.match(email) 

class SignupPage(webapp2.RequestHandler):
  def write_html(self, kwargs={}):
    name = kwargs.get('name', '')
    email = kwargs.get('email', '')

    name_err = kwargs.get('name_err', '')
    pwd_err = kwargs.get('pwd_err', '')
    email_err = kwargs.get('email_err', '')

    self.response.write(signup_html%{
                                     'name':name,
                                     'email': email,
                                     'name_err':name_err,
                                     'pwd_err':pwd_err,
                                     'email_err':email_err})

  def get(self):
    self.write_html()

  def post(self):
    name_err = ""
    pwd_err = ""
    email_err = ""

    name = self.request.get('username')
    pwd = self.request.get('password')
    verify_pwd = self.request.get('verify')
    email = self.request.get('email')
    
    if not valid_name(name): 
      name_err += "That's not a valid username."
    if not valid_pwd(pwd):
      pwd_err += "That's not a valid password."
    elif pwd != verify_pwd:
      pwd_err += "Your passwords dont match!"
    if not valid_email(email):
      email_err = "That's an invalid email."
    if name_err or pwd_err or email_err:
      self.write_html({'name_err':name_err, 
                       'pwd_err':pwd_err,
                       'email_err':email_err,
                       'name': name,
                       'email':email})
    else:
      self.redirect('/welcome?username=%s'%name)

class WelcomePage(webapp2.RequestHandler):
  def get(self):
    self.response.write('<b>Welcome, %s!</b>'%self.request.get('username'))


application = webapp2.WSGIApplication([
                                       ('/rot13', ROT13Page),
                                       ('/signup', SignupPage),
                                       ('/welcome', WelcomePage),
                                      ], debug=True)
