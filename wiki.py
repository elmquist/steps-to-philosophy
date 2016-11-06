import mwparserfromhell
import re
import requests
import sys

DEBUG = '-d' in sys.argv

def PrintD(text):
  if not DEBUG: return
  print(text[:800])


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
    return list(res['query']['pages'].values())[0]['revisions'][0]['*']


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


def FindAllLinks(text):
  p_level = 0
  in_parens = False
  b_level = 0
  in_brackets = False
  links = []
  link = ''
  for char in text:
    # This gets pretty grungy.
    # There are 2 things we care about:
    # 1. What is the first type of nested thing (brackets, parentheses) which we entered?
    # 2. When do we exit that thing (requires keeping balance)?
    #
    # So we group into those 3 states:
    # 1. we're in parenthes.
    # 2. we're in brackets.
    # 3. we're in neither, and only really care about entering one of the above.
    if in_parens:
      if char == '(':
        p_level += 1
      elif char == ')':
        p_level -= 1
        if p_level == 0:
          in_parens = False

    elif in_brackets:
      link += char

      if char == '[':
        b_level += 1
      elif char == ']':
        b_level -= 1
        if b_level == 0:
          yield link
          in_brackets = False
          link = ''

    else:
      if char == '[':
        in_brackets = True
        b_level += 1
        link += char
      elif char == '(':
        in_parens = True
        p_level += 1


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
