from datetime import datetime, timezone, timedelta

import peewee
from peewee import *
from src import creds
from src.core.mail.aprove_meets import get_message_for_users
from src.core.meets.meets import get_meetings



db = PostgresqlDatabase('postgres', host=creds.DB_HOST, port=5432, user=creds.DB_USER, password=creds.DB_PASSWORD)

class Meets(Model):
    room_uri = TextField()
    people = TextField()
    organizer = TextField()
    meet_date = DateTimeField()
    end_meet_date = DateTimeField()
    is_answered = BooleanField()
    need_process = BooleanField()
    is_processed = BooleanField()
    meet_finished = BooleanField()


    class Meta:
        database = db
        db_table = 'Meets'

db.connect()
db.create_tables([Meets])


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
        if meet.meet_date >= datetime.now(timezone.utc) and datetime.now(timezone.utc) <=meet.end_meet_date():
            # process_meet(meet)
            meet.need_process = False
            meet.is_processed = True
            meet.meet_finished = False
            meet.save()


update_meets_in_db()
search_answered()
process()




