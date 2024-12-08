from peewee import *
from src import creds

DB_CONNECTION = PostgresqlDatabase('postgres', host=creds.DB_HOST, port=5432, user=creds.DB_USER, password=creds.DB_PASSWORD)

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
        database = DB_CONNECTION
        db_table = 'Meets'

def database_migrations():

    DB_CONNECTION.connect()
    DB_CONNECTION.create_tables([Meets])