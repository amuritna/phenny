import unittest
from mock import MagicMock
from modules import issue

class TestIssue(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()
        self.input = MagicMock()
             
    def testIllegal(self):
        test = ['.issue', 'octocat/Hello-World Create an illegal issue.']
        self.assertTrue(issue.issue(test) == 'Begiak cannot create an issue there.')
        
    def testInvalid(self):
        test = ['.issue', 'boing boing boing someone is hungry']
        self.assertTrue(issue.issue(test) == 'Invalid .issue command. Usage: .issue <owner>/<repository> <title>')