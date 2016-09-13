import config
from tests.mocks import UserMock
from tests.mocks import ChatMock
from tests.mocks import MessageMock
from tests.base import BaseTestCase


class BaseTestThemesBot(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.chat = ChatMock(1)
        self.chat_2 = ChatMock(2)
        self.user = UserMock('Foo', 'Bar')
    
    def tearDown(self):
        super().tearDown()
    
    def _check(self, msg, expected_answer):
        message = MessageMock(self.chat, msg, self.user)
        self.themes_bot.route(message)
        answer = self.tele_bot.last_message.text
        self.assertEqual(answer, expected_answer)
    
    def _check_2(self, msg, expected_answer):
        message = MessageMock(self.chat_2, msg, self.user)
        self.themes_bot.route(message)
        answer = self.tele_bot.last_message.text
        self.assertEqual(answer, expected_answer)


class TestThemesBotCommon(BaseTestThemesBot):
    def test_touch(self):
        self._check('/touch foo', 'Theme №1 created')
    
    def test_ls_empty(self):
        self._check('/ls',
                    'No themes found! Discuss your shitty movies & shows!')
    
    def test_ed(self):
        self._check('/touch foo', 'Theme №1 created')
        self._check('/ed 1 bar', 'Theme 1 updated')
        self._check('/ls', '1. bar (Foo Bar)\n')
    
    def test_rm(self):
        self._check('/touch foo', 'Theme №1 created')
        self._check('/rm 1', 'Theme 1 removed')
    
    def test_rmrf(self):
        self._check('/touch foo', 'Theme №1 created')
        self._check('/touch bar', 'Theme №2 created')
        self._check('/rm -rf', 'All themes removed')
        self._check('/ls',
                    'No themes found! Discuss your shitty movies & shows!')
    
    def test_man(self):
        self._check('/man', config.help_message)


class TestThemesBotComplicated(BaseTestThemesBot):
    def test_rm_missing(self):
        self._check('/ls',
                    'No themes found! Discuss your shitty movies & shows!')
        self._check('/rm 1', 'Theme not found')
    
    def test_rmrf_missing(self):
        self._check('/ls',
                    'No themes found! Discuss your shitty movies & shows!')
        self._check('/rm -rf', 'All themes removed')
    
    def test_rm_a_few(self):
        self._check('/touch foo', 'Theme №1 created')
        self._check('/touch bar boo', 'Theme №2 created')
        self._check('/touch $%^&*(', 'Theme №3 created')
        self._check('/rm 1', 'Theme 1 removed')
        self._check('/ls', '1. bar boo (Foo Bar)\n2. $%^&*( (Foo Bar)\n')


class TestThemesBotMultipleChats(BaseTestThemesBot):
    def test_touch_two_chats(self):
        self._check('/touch apchhi', 'Theme №1 created')
        self._check_2('/touch і ў', 'Theme №1 created')
        self._check('/ls', '1. apchhi (Foo Bar)\n')
        self._check_2('/ls', '1. і ў (Foo Bar)\n')
    
    def test_rmrf_two_chats(self):
        self._check('/touch apchhi', 'Theme №1 created')
        self._check_2('/touch і ў', 'Theme №1 created')
        self._check('/rm -rf', 'All themes removed')
        self._check('/ls',
                    'No themes found! Discuss your shitty movies & shows!')
        self._check_2('/ls', '1. і ў (Foo Bar)\n')
