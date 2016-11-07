import json
import logging
import os

from google.appengine.api import memcache

import jinja2
import webapp2

import config
import wiki


class MainPage(webapp2.RequestHandler):
  def get(self):
    logging.debug(self.request)
    jinja_environment = self.jinja_environment
    template = jinja_environment.get_template("/index.html")
    self.response.out.write(template.render(self.local_config))

  @property
  def local_config(self):
    # Kind of a hack, kind of nice.
    # Define local settings you don't want published in config.py.
    return {k: vars(config)[k] for k in vars(config) if not k.startswith('_')}

  @property
  def jinja_environment(self):
    return jinja2.Environment(loader=jinja2.FileSystemLoader('./views'))


class FirstLink(webapp2.RequestHandler):
  def get(self):
    # TODO: add memcache here.
    logging.debug(self.request)
    title = self.request.get('title')
    first_link = self.get_first_link(title)
    self.response.out.write(json.dumps(({'first_link': first_link})))


  def get_first_link(self, title):
    first_link = memcache.get(title)
    if first_link is None:
      first_link = wiki.ProcessTitle(title)
      # Note: never expires.
      memcache.add(title, first_link)
    return first_link


  @property
  def jinja_environment(self):
    return jinja2.Environment(loader=jinja2.FileSystemLoader('./views'))


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/firstlink/', FirstLink),
], debug=True)
