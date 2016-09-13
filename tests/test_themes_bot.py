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
    
    def test_ls_empty(self):
        text = '/ls'
        message = MessageMock(self.chat, text, self.user)
        self.themes_bot.route(message)
        answer = self.tele_bot.last_message.text
        self.assertEqual(
            answer, 'No themes found! Discuss your shitty movies & shows!')
    
    def test_touch(self):
        text = '/touch foo'
        message = MessageMock(self.chat, text, self.user)
        self.themes_bot.route(message)
        answer = self.tele_bot.last_message.text
        self.assertEqual(
            answer, 'Theme №1 created')
