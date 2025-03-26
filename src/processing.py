import json
from datetime import datetime
from src.database.SQl.database_controller import Meets
import caldav
import re
import src.creds as creds
import peewee
import requests


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
                people = json.dumps(meet.people),
                organizer = meet.organizer,
                meet_date=meet.meet_date,
                end_meet_date=meet.end_meet_date,
                is_answered = False,
                need_process = False,
                is_processed = False,
                meet_finished = None
                )
            new_meet.save()
            print('Встреча была успешна сохранена в базу данных ')

def mail(meet):
    data = {'to': [meet.organizer], 'subject': "Потверждение встречи", "body": f"Встреча была приянта на :{meet.meet_date},бот сможет подключиться к видеоконференции."}
    response  = requests.post("http://localhost:8000/send-email", json=data)
    print(response.text)


def search_answered():
    for meet in Meets.select().where(Meets.is_answered == False):

        mail(meet)
        print('Письмо с подтверждением подключения к конференции было успешно доставлено')
        meet.is_answered = True
        meet.need_process = True
        meet.save()


def connect_on_meet():
    for meet in Meets.select().where(Meets.need_process == True):
        if meet.meet_date <= datetime.now() <= meet.end_meet_date:
            print('Программа начинает подключение к конференции')
            response = requests.get(f"http://localhost:80/connect/{meet.room_uri[21:]}")
            print(response.text)
            meet.need_process = False
            meet.is_processed = True
            meet.save()
            print("Подключение к конференции было супешно завершенно")







