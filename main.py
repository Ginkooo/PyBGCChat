import time

from fbchat import Client, log
from fbchat.models import Message, ThreadType
import weather

from config import FBPASS, FBUSER, CHATNAME, CITY
from utils import far2cel


class FBBot(Client):

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

    def pogoda(self, thread_id):
        weather_obj = weather.Weather()
        location = weather_obj.lookup_by_location(CITY)
        forecasts = location.forecast()
        for forecast in forecasts[:3]:
            min = round(far2cel(int(forecast.low())))
            max = round(far2cel(int(forecast.high())))
            text = forecast.text()
            date = forecast.date()
            msg = Message(text=f'Pododa na {date}: Od {min} do {max} stopni, {text}')
            self.send(msg, thread_id=self.thread_id_, thread_type=ThreadType.GROUP)


client = FBBot(CHATNAME, FBUSER, FBPASS)

stillborn = client.searchForGroups(CHATNAME)[0]

client.send(Message('Bot zwarty i gotowy do działania'), thread_id=stillborn.uid, thread_type=ThreadType.GROUP)

client.listen()
