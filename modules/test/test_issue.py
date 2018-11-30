import unittest, json
from mock import MagicMock, patch
from modules import issue

class TestIssue(unittest.TestCase):
    
    def setUp(self):
        self.phenny = MagicMock()
        self.input = MagicMock()
        self.phenny.nick = 'phenny'
        
    @patch('modules.issue.post')
    def test_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'html_url': 'https://github.com/test/test'
        }
        mock_post.return_value = mock_response
        self.input.group.return_value = mock_response
        
        mock_body = json.dumps({ "title": "Create a test issue.", "body": "This issue was automatically made by begiak, Apertium\'s beloved IRC bot, by the order of phenny on #apertium. A human is yet to update the description."})
        mock_head = {'Authorization': 'token {}'.format(self.phenny.config.gh_oauth_token)}
        mock_post.assert_called_with('https://api.github.com/repos/test/test/issues', mock_body, mock_head)
        self.input.group = lambda x: ['.issue' 'test/test Create a test issue.'][x]
        
        issue.issue(self.phenny, self.input)
        self.phenny.reply.assert_called_with('Issue created. You can add a description at https://github.com/test/test')
             
    def test_illegal(self):
        self.input.group = lambda x: ['.issue', 'octocat/Hello-World Create an illegal issue.']
        self.input.group.return_value = 'Begiak cannot create an issue there.'
        issue.issue(self.phenny, self.input)
        self.phenny.reply.assert_called_with('Begiak cannot create an issue there.')
        
    def test_invalid(self):
        self.input.group = lambda x: ['.issue', 'boing boing boing someone is hungry']
        self.input.group.return_value = 'Invalid .issue command. Usage: .issue <owner>/<repository> <title>'
        issue.issue(self.phenny, self.input)
        self.phenny.reply.assert_called_with('Invalid .issue command. Usage: .issue <owner>/<repository> <title>')
