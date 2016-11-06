import sys

import wiki


def FindPage(start, end='Philosophy'):
  current = start
  path = []
  while True:
    print('-> %s' % current)
    path.append(current)
    if current.lower() == end.lower():
      break
    if path.count(current) > 1:
      print('found a loop!')
      print(path)
      break
    current = wiki.ProcessTitle(current)


if __name__ == '__main__':
  FindPage(sys.argv[1])
