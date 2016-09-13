import config
from tests.mocks import UserMock
from tests.mocks import ChatMock
from tests.mocks import MessageMock
from tests.base import BaseTestCase


class TestThemesBot(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.chat = ChatMock(1)
        self.user = UserMock('Foo', 'Bar')
    
    def tearDown(self):
        super().tearDown()
    
    def _check(self, msg, expected_answer):
        message = MessageMock(self.chat, msg, self.user)
        self.themes_bot.route(message)
        answer = self.tele_bot.last_message.text
        self.assertEqual(answer, expected_answer)
    
    def test_touch(self):
        answer = self._check('/touch foo', 'Theme №1 created')
    
    def test_ls_empty(self):
        answer = self._check(
            '/ls', 'No themes found! Discuss your shitty movies & shows!')
    
    def test_ed(self):
        answer = self._check('/touch foo', 'Theme №1 created')
        answer = self._check('/ed 1 bar', 'Theme 1 updated')
        answer = self._check('/ls', '1. bar (Foo Bar)\n')
    
    def test_rm(self):
        answer = self._check('/touch foo', 'Theme №1 created')
        answer = self._check('/rm 1', 'Theme 1 removed')
    
    def test_rmrf(self):
        answer = self._check('/touch foo', 'Theme №1 created')
        answer = self._check('/touch bar', 'Theme №2 created')
        answer = self._check('/rm -rf', 'All themes removed')
        answer = self._check(
            '/ls', 'No themes found! Discuss your shitty movies & shows!')
    
    def test_man(self):
        answer = self._check('/man', config.help_message)
