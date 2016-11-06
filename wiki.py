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
  level = 0
  links = []
  link = ''
  for char in text:
    if char == '[':
      level += 1
      link += char
    elif char == ']':
      level -= 1
      link += char
      if level == 0:
        links.append(link)
        link = ''
    elif level > 0:
      link += char
  return links


def Clean(text):
  text = RemoveTemplates(text)
  text = RemoveParentheses(text)
  return text.strip()


def NormalizeTitle(title):
  title = title.lower()
  title = title.replace(' ', '_')
  return title


def FindFirstLink(text):
  PrintD('raw text\n\n' + text)
  text = Clean(text)
  PrintD('clean text\n\n' + text)
  links = FindAllLinks(text)
  for link in links:
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
