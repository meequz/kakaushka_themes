
class ChatMock(object):
    def __init__(chat_id):
        self.id = chat_id


class MessageMock(object):
    def __init__(chat_id, text):
        self.chat = ChatMock(chat_id)
        self.text = text


class TeleBotMock(object):
    def __init__(self, token):
        self.token = token
        self.last_message = None
    
    def send_message(self, chat_id, text, **kwargs):
        self.last_message = MessageMock(chat_id, text)
