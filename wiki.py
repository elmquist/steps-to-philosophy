import mwparserfromhell
import re
import requests
import sys

DEBUG = '-d' in sys.argv

def PrintD(text):
  if not DEBUG: return
  print(text[:800])


class InvalidTitleException(BaseException): pass


def FetchRaw(title):
    API_URL = 'https://en.wikipedia.org/w/api.php'
    data = {
        'action': 'query',
        'prop': 'revisions',
        'rvlimit': 1,
        'rvprop': 'content',
        'format': 'json',
        'titles': title,
    }
    res = requests.get(API_URL, params=data).json()
    try:
      return list(res['query']['pages'].values())[0]['revisions'][0]['*']
    except KeyError:
      raise InvalidTitleException('Wikipedia page not found ' + title)


def RemoveTemplates(text):
  parsed = mwparserfromhell.parse(text)
  for template in parsed.filter_templates():
    try: parsed.remove(template)
    except ValueError: pass
  return parsed


def RemoveParentheses(text):
  level = 0
  ret = ''
  for char in text:
    if char == '(':
      level += 1
    elif char == ')':
      level -= 1
    elif level == 0:
      ret += char
  return ret


class LinkFinder():
  def __init__(self, text):
    self.text = text
    self.p_level = 0
    self.in_parens = False
    self.b_level = 0
    self.in_brackets = False
    self.link = ''


  # We're in parentheses. We only really care about getting out of here.
  def StepParens(self, char):
    if char == '(':
      self.p_level += 1
    elif char == ')':
      self.p_level -= 1
      if self.p_level == 0: self.in_parens = False


  # We're in brackets! Keep track of the current link (self.link), in addition
  # to our bracket level (remember nesting), so we know when to exit (the end
  # of the link).
  # This returns the link if it is completed (otherwise doesn't return
  # anything).
  def StepBrackets(self, char):
    self.link += char
    if char == '[':
      self.b_level += 1
    elif char == ']':
      self.b_level -= 1
      # We reached the end of the link. Return it and tidy up.
      if self.b_level == 0:
        link = self.link
        self.in_brackets = False
        self.link = ''
        return link


  # We're in neither parentheses nor brackets. We only care about entering one
  # of the above from here.
  def Step(self, char):
    if char == '[':
      self.in_brackets = True
      self.b_level += 1
      # Start saving the current link.
      self.link += char
    elif char == '(':
      self.in_parens = True
      self.p_level += 1


  def FindAllLinks(self):
    for char in self.text:
      # We keep track of the *first* type of thing that we enter (parentheses, brackets).
      # There can (and will) be nesting within this.
      # So we group into handling the 3 states:
      # 1. We're in parenthes.
      # 2. We're in brackets.
      # 3. We're in neither.
      if self.in_parens:
        self.StepParens(char)
      elif self.in_brackets:
        link = self.StepBrackets(char)
        # If we finished the current link, yield it to the caller.
        if link: yield link
      else:
        self.Step(char)



def FindAllLinks(text):
  return LinkFinder(text).FindAllLinks()


def Clean(text):
  text = RemoveTemplates(text)
  return text.strip()


def NormalizeTitle(title):
  title = title.lower()
  title = title.replace(' ', '_')
  return title


def FindFirstLink(text):
  PrintD('raw text\n\n' + text)
  text = Clean(text)
  PrintD('clean text\n\n' + text)
  for link in FindAllLinks(text):
    if re.match('\S+:.*', link):
      PrintD('skipping non-wiki link %s' % link)
      continue
    link = link.split('|')[0]
    link = link.strip('[[')
    link = link.rstrip(']]')
    link = NormalizeTitle(link)
    return link


def ProcessTitle(title):
  text = FetchRaw(title)
  first_link = FindFirstLink(text)
  return first_link


if __name__ == '__main__':
  print(ProcessTitle(sys.argv[1]))
