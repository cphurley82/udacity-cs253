#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2

import os.path

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

# def escape_html(s):
#     return cgi.escape(s, quote=True)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **key_words):
        self.response.out.write(render_str(template, **key_words))



main_form="""
<form action="http://www.google.com/search">
    <input name="q">
    <input type="submit">
</form>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(main_form)

class Rot13Handler(BaseHandler):
    def get(self):
        self.render('rot13-form.html')
        
    def post(self):
        user_text=self.request.get('text')
        rot13 = user_text.encode('rot13')
        self.render('rot13-form.html', text = rot13)

import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)
  
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)
  
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

class SignupHandler(BaseHandler):
    def get(self):
        self.render('signup-form.html')
    def post(self):
        valid_entry=True
        username = self.request.get("username")
        username_error = ""
        if not valid_username(username):
            username_error="That's not a valid username."
            valid_entry=False
        
        password = self.request.get("password")
        password_error = ""
        if not valid_password(password):
            password_error="That wasn't a valid password."
            valid_entry=False
            
        verify_password = self.request.get("verify")
        verify_password_error = ""
        if verify_password != password:
            verify_password_error="Your passwords didn't match."
            valid_entry=False
            
        email = self.request.get("email")
        email_error = ""
        if email != "" and not valid_email(email):
            email_error="That's not a valid email."
            valid_entry=False
        if(valid_entry):
            self.redirect('/unit2/welcome?username='+username) #
        else:
            params = dict(username=username,
                         error_username=username_error,
                         error_password=password_error,
                         error_verify=verify_password_error,
                         email=email,
                         error_email=email_error)
            self.render('signup-form.html', **params)        
        

welcome_form="""
<!DOCTYPE html>

<html>
  <head>
    <title>Unit 2 Signup</title>
  </head>

  <body>
    <h2>Welcome, %(username)s!</h2>
  </body>
</html>
"""

def write_welcome_form(username):
    return welcome_form % {"username":username}

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.write(write_welcome_form(username))

class FizzBuzzHandler(BaseHandler):
    def get(self):
        self.render('fizzbuzz.html', n=15)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/unit2/rot13', Rot13Handler),
    ('/unit2/signup', SignupHandler),
    ('/unit2/welcome', WelcomeHandler),
    ('/unit2/fizzbuzz', FizzBuzzHandler),
], debug=True)
