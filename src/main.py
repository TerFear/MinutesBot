from src.database.database_controller import database_migrations
from src.processing import update_meets_in_db, search_answered, process

# Создать таблицы в БД
database_migrations()


while True:
    # Получить заново весь список собраний и добавить в БД новые
    update_meets_in_db()
    # Ищем все сообщения по которым мы еще не давали подтверждения
    search_answered()
    # Ищем все которые надо обработать и запускаем обработку
    process()
