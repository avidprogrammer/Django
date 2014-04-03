import webapp2
from cgi import escape as cgi_esc

def esc_html(args):
    return cgi_esc(args, quote=True)

form="""
<form method="post">
    What is your birthday?
    <br>
    <label> Month <input name="month" value=%(month)s> </label>
    <label> Day <input name="day" value=%(day)s> </label>
    <label> Year <input name="year" %(year)s> </label>
    <br>
    <div style="{color:red}">%(error)s</div>
    <br>
    <input type="submit" value="submit">
</form>
"""

def valid_month(month):
    if month:
        month = month.capitalize()
        if month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                     'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            return month

def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if (day > 0) and (day < 32):
            return day

def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if (year >= 1990) and (year < 2020):
            return year

def validate_request(month, day, year):
    if (valid_month(month) and valid_day(day) and valid_year(year)):
        return True    

class MainPage(webapp2.RequestHandler):
    
    def write_form(self, error="", month="", year="", day=""):
        self.response.write(form%{'error': error,
                                  'month': esc_html(month),
                                  'year': esc_html(year),
                                  'day': esc_html(day)})  
 
    def get(self):
        self.write_form()

    def post(self):
        month = self.request.get('month')
        day = self.request.get('day')
        year = self.request.get('year')
        valid = validate_request(month, day, year)
        if valid:
            self.redirect('/success')
        else:
            self.write_form(error="Invalid input", month=month, day=day, 
                                                                year=year)

class Success(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Nicely done!')

application = webapp2.WSGIApplication([('/', MainPage),
                                       ('/success', Success),
                                      ],
                                      debug=True)

