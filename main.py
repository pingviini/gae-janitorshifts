#!/usr/bin/env python

import cgi
import webapp2
import jinja2
import os


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainHandler(webapp2.RequestHandler):

    def get(self):
        template_values = {}

        if cgi.escape(self.request.get('asunnot')):
            template_values['asunnot'] = cgi.escape(
                self.request.get('asunnot'))

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
