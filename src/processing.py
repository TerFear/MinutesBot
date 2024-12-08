from datetime import datetime, timezone
from src.database.database_controller import Meets
from src.mail.aprove_meets import get_message_for_users
import caldav
import re
import src.creds as creds
import peewee
from src.conference.conference_connector import meet_on_telemost
from src.mail.send_email import send_email
from src.ml_models.speech_to_text import speech
from src.ml_models.text_summarization import processing

class MeetPattern:
    def __init__(self, pattern, provider):
        self.pattern = pattern
        self.provider = provider


class CalendarMeet:
    def __init__(self):
        self.event_uri = None
        self.description = None
        self.meet_date = None
        self.room_uri = None
        self.room_provider = None
        self.organizer = None
        self.people = None
        self.is_processed = None
        self.is_answered = None
        self.need_process = None
        self.end_meet_date = None


def process_meet(meet):
    """Подключиться к собранию и обработать его"""

    # Подключились ко встрече (Selenim)
    meet_on_telemost(meet)

    # Распознали текст из файла (openai/whisper-large-v3-turbo)
    text = speech(meet)

    # Подведение итогов встречи (ChatGPT/Llama)
    summary = processing(text)

    # Отправка итогов встерчи по почте (SMTPLib)
    send_email(summary, meet)

    meet.meet_finished = True
    meet.save()


def find_room(description):
    """ Найти комнату в которой будет проходить митинг """

    meets_patterns = [
        MeetPattern(r'telemost.yandex.ru/j/\d{14}', 'yandex'),
        MeetPattern(r'meet.google.com/\w{3}-\w{4}-\w{3}', 'google')
    ]
    for pattern in meets_patterns:
        uri = re.search(pattern.pattern, description)
        if uri:
            return uri[0], pattern.provider
    return None


def get_meetings():
    dav = caldav.DAVClient(
        url=creds.SERVER_CALENDAR,
        username=creds.EMAIL,
        password=creds.PASSWORD_CALENDAR)

    with dav as client:
        calendar = client.principal().calendars()[0]
        events_fetched = calendar.search(
            start=datetime(2024, 12, 6),
            end=datetime(2025, 12, 1),
            event=True,
            expand=True
        )

    meets = []
    for event in events_fetched:
        meet = CalendarMeet()
        meet.people = []
        meet.event_uri = event.url
        meet.description = event.vobject_instance.vevent.description.value
        meet.meet_date = event.vobject_instance.vevent.dtstart.value
        meet.end_meet_date = event.vobject_instance.vevent.dtend.value
        meet.organizer = event.vobject_instance.vevent.organizer.value[7:]
        for item in event.vobject_instance.vevent.contents['attendee']:
            if not item.value[7:] == 'minutesbot@yandex.ru':
                meet.people.append(item.value[7:])
        room_info = find_room(meet.description)
        if room_info:
            meet.room_uri = room_info[0]
            meet.room_provider = room_info[1]
        meets.append(meet)
    return meets


def update_meets_in_db():
    loaded_meets = get_meetings()
    for meet in loaded_meets:
        try:
            Meets.get(Meets.room_uri == meet.room_uri)
        except peewee.DoesNotExist:
            new_meet = Meets(
                room_uri = meet.room_uri,
                people = meet.people,
                organizer = meet.organizer,
                meet_date=meet.meet_date,
                end_meet_date=meet.end_meet_date,
                is_answered = False,
                need_process = False,
                is_processed = False,
                meet_finished = None
                )
            new_meet.save()


def search_answered():
    for meet in Meets.select().where(Meets.is_answered == False):
        get_message_for_users(meet)
        meet.is_answered = True
        meet.need_process = True
        meet.save()


def process():
    for meet in Meets.select().where(Meets.need_process == True):
        if meet.meet_date <= datetime.now() <= meet.end_meet_date:
            process_meet(meet)
            meet.need_process = False
            meet.is_processed = True
            meet.meet_finished = False
            meet.save()

