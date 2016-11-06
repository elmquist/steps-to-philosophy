import sys

import wiki


def AddTest(title):
  print('Adding e2e test for %s' % title)
  print('Fetching raw text')
  raw_text = wiki.FetchRaw(title)
  print(raw_text[:600])
  print('\n\n')
  print('open this link and find the first link')
  print('http://en.wikipedia.org/wiki/%s' % title)
  first_link = input('Expected first link: ')
  test_input_file = './e2e_tests/%s.input' % title
  print('writing input to %s' % test_input_file)
  with open(test_input_file, 'w') as f:
    f.write(raw_text)
  test_output_file = './e2e_tests/%s.expected' % title
  print('writing expected output to %s' % test_output_file)
  with open(test_output_file, 'w') as f:
    f.write(first_link)
  print('done!')


if __name__ == '__main__':
  AddTest(sys.argv[1])
