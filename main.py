import json
import logging
import os

import jinja2
import webapp2

import wiki


class MainPage(webapp2.RequestHandler):
  def get(self):
    logging.debug(self.request)
    jinja_environment = self.jinja_environment
    template = jinja_environment.get_template("/index.html")
    self.response.out.write(template.render())

  @property
  def jinja_environment(self):
    return jinja2.Environment(loader=jinja2.FileSystemLoader('./views'))


class GetFirstLink(webapp2.RequestHandler):
  def get(self):
    # TODO: add memcache here.
    logging.debug(self.request)
    title = self.request.get('title')
    self.response.out.write(json.dumps(({'first_link': wiki.ProcessTitle(title)})))

  @property
  def jinja_environment(self):
    return jinja2.Environment(loader=jinja2.FileSystemLoader('./views'))

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/getfirstlink/', GetFirstLink),
], debug=True)
