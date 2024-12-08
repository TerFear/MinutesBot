from src.core.meets.get_meetings import update_meets_in_db, search_answered, process

while True:
    # Получить заново весь список собраний и добавить в БД новые
    update_meets_in_db()
    # Ищем все сообщения по которым мы еще не давали подтверждения
    search_answered()
    # Ищем все которые надо обработать и запускаем обработку
    process()
