import time

from fbchat import Client, log
from fbchat.models import Message, ThreadType

from config import FBPASS, FBUSER, CHATNAME


class WeatherBot(Client):

    def __init__(self, group_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread_id_ = self.searchForGroups(group_name)[0].uid

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        if not thread_id == self.thread_id_:
            log.info('Message is not sent in a group thread')
            return

        if not message_object.text.startswith('!'):
            log.info('Message is not a command')
            return

        func = message_object.text[1:]

        log.info(f'Invoking: {func}')

        try:
            func = getattr(self, func)
        except AttributeError:
            log.info(f'There is not such function as {func}')

        func(self.thread_id_)

    def godzina(self, thread_id):
        curr_time = time.strftime('%H:%M:%S')
        msg = Message(text=f'Jest godzina: {curr_time}')
        self.send(msg, thread_id=thread_id, thread_type=ThreadType.GROUP)


client = WeatherBot(CHATNAME, FBUSER, FBPASS)

stillborn = client.searchForGroups(CHATNAME)[0]

client.send(Message('Spytaj się mnie o godzinę'), thread_id=stillborn.uid, thread_type=ThreadType.GROUP)

client.listen()
