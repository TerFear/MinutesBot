
from src.processing import update_meets_in_db, connect_on_meet
from src.processing import search_answered


while True:
    update_meets_in_db()
    search_answered()
    connect_on_meet()