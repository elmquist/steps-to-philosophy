import unittest

import wiki

class RemoveParenthesesTests(unittest.TestCase):

  TEST_CASES = [
      ('', ''),
      ('()', ''),
      ('()()', ''),
      ('(())', ''),
      ('hi ()', 'hi '),
      ('() hi', ' hi'),
      ('( hi )', ''),
      ('(hi)', ''),
      ('hello(hi (there) (what (what)))', 'hello'),
  ]

  def test_list(self):
    for test_input, expected in self.TEST_CASES:
      self.assertEqual(wiki.RemoveParentheses(test_input), expected)


if __name__ == '__main__':
  unittest.main()
