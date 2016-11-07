import unittest

import wiki

class FindAllLinksTest(unittest.TestCase):

  TEST_CASES = [
      ('', []),
      ('hi there', []),
      ('[[link]]', ['[[link]]']),
      ('I am a [[link]]', ['[[link]]']),
      ('I have [[two]] [[links]]', ['[[two]]', '[[links]]']),
      ('I am a [[link with spaces]]', ['[[link with spaces]]']),
      ('skip this ([[link]])', []),
      ('skip this ([[link]]) but not this [[one]]', ['[[one]]']),
      ('skip this {{[[link]]}}', []),
      ('skip this {{[[link]]}} but not this [[one]]', ['[[one]]']),
      ('[[links can have (parentheses)]]', ['[[links can have (parentheses)]]']),
      ('[[links can have [[other links]] maybe?]]',
        ['[[links can have [[other links]] maybe?]]']),
      ('[[links can have {{templates}} maybe?]]',
        ['[[links can have {{templates}} maybe?]]']),
  ]

  def test_list(self):
    for test_input, expected in self.TEST_CASES:
      self.assertEqual(list(wiki.FindAllLinks(test_input)), expected)


if __name__ == '__main__':
  unittest.main()
