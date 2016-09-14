import unittest

import config
from bot import MongoStorage
from bot import ThemesStorage
from bot import ThemesManager
from bot import ThemesBot
from tests.mocks import TeleBotMock


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.db_storage = MongoStorage(config.mongo_db_name,
                                       config.mongo_test_collection_name)
        themes_storage = ThemesStorage(self.db_storage)
        themes_manager = ThemesManager(themes_storage)
        
        self.tele_bot = TeleBotMock('')
        self.themes_bot = ThemesBot(self.tele_bot, themes_manager)

    def tearDown(self):
        self.db_storage.drop()
