from tests.mocks import ChatMock
from tests.mocks import MessageMock
from tests.base import BaseTestCase


class TestThemesBot(BaseTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_ls_empty(self):
        chat = ChatMock(1)
        text = '/ls'
        message = MessageMock(chat, text)
        self.themes_bot.route(message)
        answer = self.tele_bot.last_message.text
        self.assertEqual(
            answer, 'No themes found! Discuss your shitty movies & shows!')
