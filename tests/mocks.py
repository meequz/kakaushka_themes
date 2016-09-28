class UserMock(object):
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class ChatMock(object):
    def __init__(self, chat_id):
        self.id = chat_id


class MessageMock(object):
    def __init__(self, chat, text, user):
        self.chat = chat
        self.text = text
        self.from_user = user


class TeleBotMock(object):
    def __init__(self, token):
        self.token = token
        self.last_message = MessageMock(None, None, None)
    
    def send_message(self, chat_id, text, **kwargs):
        chat = ChatMock(chat_id)
        self.last_message = MessageMock(chat, text, None)
