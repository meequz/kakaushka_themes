import unittest

import config
from bot import MongoStorage
from bot import ThemesStorage
from bot import ThemesManager
from bot import ThemesBot
from tests.mocks import TeleBotMock


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.tele_bot = TeleBotMock('')
        db_storage = MongoStorage(config.mongo_db_name,
                                  config.mongo_test_collection_name)
        themes_storage = ThemesStorage(db_storage)
        themes_manager = ThemesManager(themes_storage)
        self.themes_bot = ThemesBot(self.tele_bot, themes_manager)
