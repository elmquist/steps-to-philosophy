import glob
import os

import wiki


def ReadFile(filename):
  with open(filename, 'r') as f:
    return f.read().strip()


def RunTests():
  input_files = glob.glob('e2e_tests/*.input')
  results = []
  for input_file in input_files:
    test_input = ReadFile(input_file)
    expected_file = os.path.splitext(input_file)[0] + '.expected'
    expected = ReadFile(expected_file)
    expected = wiki.NormalizeTitle(expected)
    actual = wiki.FindFirstLink(test_input)
    if actual == expected:
      results.append({'pass': True})
    else:
      results.append({
        'pass': False,
        'input': input_file,
        'expected': expected,
        'actual': actual,
      })
  print('Ran %d tests' % len(results))
  for result in results:
    if result['pass']: continue
    print('Failure: input: %s expected: %s actual: %s' % (
      result['input'], result['expected'], result['actual']))


if __name__ == '__main__':
  RunTests()
