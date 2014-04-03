import webapp2
from cgi import escape as cgi_esc

html = """
<form method="post">
    <textarea tows="4" cols="50" name="text" />%(content)s</textarea>
    <br>
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

class MainPage(webapp2.RequestHandler):

    def write_html(self, content=""):
        self.response.write(html%{'content' : cgi_esc(content, quote=True)})

    def get(self):
        self.write_html()

    def post(self):
        text = self.request.get('text')
        self.write_html(text_manip(text))

application = webapp2.WSGIApplication([('/', MainPage),
                                      ], debug=True)
