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

import os
from google.appengine.ext.webapp import template
import wsgiref.handlers
import sys 

from google.appengine.ext import webapp

class Story:
  pass
  
class MainHandler(webapp.RequestHandler):

  def get(self, path):
    if path == '':
      stories = []
      for item1 in os.listdir(os.path.join(os.path.dirname(__file__), 'site/2008')):
        for item2 in os.listdir(os.path.join(os.path.join(os.path.dirname(__file__), 'site/2008'), item1)):
          for item3 in os.listdir(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__), 'site/2008'), item1), item2)):          
            stories.append(''.join(['2008/', item1, '/', item2, '/', item3]))
      stories.sort()
      stories.reverse()
      
      data = []
      for story in stories:
        s = Story()
        s.lines = []
        file = open(os.path.join(os.path.dirname(__file__), ''.join(['site/', story])))
        count = 0
        while 1:
          line = file.readline()
          if count == 4:
            s.title = line
          if not line or line == "<!-- break -->\n":
            break
          if count > 4:
            s.lines.append(line)
          count = count + 1
        s.url = story
        data.append(s)
        
      path = os.path.join(os.path.dirname(__file__), 'site/index.html')
      self.response.out.write(template.render(path, { 'stories': data }))
    else:      
      if path.endswith('/'):
        path = path[0:-1]
        path = ''.join(['site/',path])
        path = os.path.join(os.path.dirname(__file__), path)
        if os.path.exists(path):
          self.response.out.write(template.render(path, {}))
        else:
          self.error(404)
          self.response.out.write(template.render('404.html', {}))
      else:
        self.redirect(''.join(['/', path, '/']), permanent=True)


def main():
  application = webapp.WSGIApplication([('/(.*)', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
