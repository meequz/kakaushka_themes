import time
import logging

import telebot
import pymongo

import config


class MongoStorage(object):
    """
    Wrapper for MongoDB
    """
    
    def __init__(self, db_name, collection_name):
        self.client = pymongo.MongoClient()
        self.db_name = db_name
        self.collection_name = collection_name
        self.db = getattr(self.client, db_name)
        self.collection = getattr(self.db, collection_name)
    
    def create(self, entry):
        return self.collection.insert_one(entry)
    
    def update(self, pattern, update):
        return self.collection.update_many(pattern, update)
    
    def update_one(self, pattern, update):
        return self.collection.update_one(pattern, update)
    
    def count(self, pattern=None):
        return self.collection.count(pattern)
    
    def find(self, pattern=None):
        return self.collection.find(pattern)
    
    def find_one(self, pattern=None):
        return self.collection.find_one(pattern)
    
    def delete(self, pattern):
        return self.collection.delete_many(pattern)
    
    def delete_one(self, pattern):
        return self.collection.delete_one(pattern)
    
    def drop(self):
        return self.db.drop_collection(self.collection_name)


class ThemesStorage(object):
    """
    It implements storage logic.
    Responsible for storing operations and format.
    """
    
    def __init__(self, db_storage):
        self.db_storage = db_storage
    
    def save(self, text, author, chat_id):
        num = self.db_storage.count({'chat': chat_id}) + 1
        self.db_storage.create({'num': num, 'text': text, 'author': author,
                                'chat': chat_id})
        return num
    
    def count(self, chat_id):
        return self.db_storage.count({'chat': chat_id})
    
    def list(self, chat_id):
        return [theme for theme in self.db_storage.find({'chat': chat_id})]
    
    def update(self, num, new_text, author, chat_id):
        self.db_storage.update_one(
            {'num': num, 'chat': chat_id},
            {'$set': {'text': new_text, 'author': author}}
        )
    
    def remove(self, num, chat_id):
        res = self.db_storage.delete_one({'num': num, 'chat': chat_id})
        self.db_storage.update({'num': {'$gt': num}, 'chat': chat_id},
                               {'$inc': {'num': -1}})
        return res.deleted_count
    
    def remove_all(self, chat_id):
        self.db_storage.delete({'chat': chat_id})


class ThemesManager(object):
    """
    Parses the incoming messages and call appropriate storage methods.
    """
    
    def __init__(self, themes_storage):
        self.themes_storage = themes_storage
    
    def _get_author(self, message):
        return '{} {}'.format(message.from_user.first_name,
                              message.from_user.last_name)
    
    def new(self, message):
        msg_splitted = message.text.split(' ')
        theme = ' '.join(msg_splitted[1:])
        author = self._get_author(message)
        num = self.themes_storage.save(theme, author, message.chat.id)
        return num
    
    def list(self, message):
        all_themes = self.themes_storage.list(message.chat.id)
        return sorted(all_themes, key=lambda x: x['num'])
    
    def update(self, message):
        msg_splitted = message.text.split(' ')
        num = int(msg_splitted[1])
        theme = ' '.join(msg_splitted[2:])
        author = self._get_author(message)
        self.themes_storage.update(num, theme, author, message.chat.id)
        return num
    
    def remove(self, message):
        msg_splitted = message.text.split(' ')
        num = int(msg_splitted[1])
        deleted_count = self.themes_storage.remove(num, message.chat.id)
        return num, deleted_count
    
    def remove_all(self, message):
        self.themes_storage.remove_all(message.chat.id)


class ThemesBot(object):
    """
    Generates correct answer according to manager returned values.
    """
    
    def __init__(self, tele_bot, manager):
        self.tele_bot = tele_bot
        self.manager = manager
    
    def _send(self, chat_id, text, plain=False):
        if plain:
            self.tele_bot.send_message(chat_id, text)
        else:
            self.tele_bot.send_message(chat_id, text, parse_mode="Markdown")
    
    def _send_and_log(self, chat_id, text):
        self._send(chat_id, text)
        logging.warning(text)
    
    def touch(self, message):
        num = self.manager.new(message)
        text = 'Theme №{} created'.format(num)
        self._send_and_log(message.chat.id, text)
    
    def ls(self, message):
        text = ''
        for theme in self.manager.list(message):
            text += '{num}. {text} ({author})\n'.format(**theme)
        if not text:
            text = 'No themes found! Discuss your shitty movies & shows!'
        self._send(message.chat.id, text)
    
    def ed(self, message):
        num = self.manager.update(message)
        text = 'Theme {} updated'.format(num)
        self._send_and_log(message.chat.id, text)
    
    def rm(self, message):
        num, deleted_count = self.manager.remove(message)
        if deleted_count == 0:
            text = 'Theme not found'
        elif deleted_count == 1:
            text = 'Theme {} removed'.format(num)
        else:
            raise Exception('Hmm, deleted more than one theme...')
        self._send_and_log(message.chat.id, text)
    
    def rmrf(self, message):
        self.manager.remove_all(message)
        text = 'All themes removed'
        self._send_and_log(message.chat.id, text)
    
    def man(self, message):
        self._send(message.chat.id, config.help_message, plain=True)
    
    def route(self, message):
        msg = message.text
        
        if msg.startswith(('/touch ', '/t ')):
            self.touch(message)
        
        if msg in ('/ls', '/l'):
            self.ls(message)
        
        if msg.startswith(('/ed ', '/e ')):
            self.ed(message)
        
        if msg in ('/rm -rf', '/rm -rf /'):
            self.rmrf(message)
        elif msg.startswith(('/rm ', '/r ')):
            self.rm(message)
        
        if msg in ('/man', '/m', '/help', '/h'):
            self.man(message)


def init():
    logging.basicConfig(format='%(asctime)s    %(message)s')
    logging.warning('Starting bot...')
    
    tele_bot = telebot.TeleBot(config.token)
    db_storage = MongoStorage(config.mongo_db_name,
                              config.mongo_collection_name)
    themes_storage = ThemesStorage(db_storage)
    themes_manager = ThemesManager(themes_storage)
    themes_bot = ThemesBot(tele_bot, themes_manager)
    
    logging.warning('{} bot started'.format(config.bot_name))
    return tele_bot, themes_bot


def main():
    tele_bot, themes_bot = init()
    
    @tele_bot.message_handler(content_types=['text'])
    def process_message(message):
        # report if there are message processing problems
        try:
            themes_bot.route(message)
        except Exception as e:
            answer = 'Some error happened:\n{}'.format(str(e))
            tele_bot.send_message(message.chat.id, answer)
            logging.exception('"{}": {}'.format(message.text, str(e)))
    
    # if some network problem, wait and restart bot
    try:
        tele_bot.polling(none_stop=True)
    except Exception as e:
        logging.exception(str(e))
        time.sleep(5)
        main()


if __name__ == '__main__':
    main()
