import sys

import wiki


def FindPage(start, end='Philosophy'):
  current = start
  path = []
  while current.lower() != end.lower():
    path.append(current)
    if path.count(current) > 1:
      print 'found a loop!'
      print path
      break
    print 'WIKI PAGE %s' % current
    current = wiki.ProcessTitle(current)


if __name__ == '__main__':
  print FindPage(sys.argv[1])

