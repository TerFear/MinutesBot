from datetime import datetime
import caldav
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import src.creds as creds


class MeetPattern:
    def __init__(self, pattern, provider):
        self.pattern = pattern
        self.provider = provider


class Meet:
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
    """ Получение встреч из календаря """

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
        meet = Meet()
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




get_meetings()