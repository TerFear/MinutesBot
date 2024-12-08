from src.core.audio.audio import audio
from src.core.meets.meet_connector import meet_on_telemost
from src.core.mail.send_email import send_email
from src.core.audio.spech_text import speech
from src.core.meets.text_processing import processing


def process_meet(meet):
    """Подключиться к собранию и обработать его"""

    # Подключились ко встрече (Selenim)
    meet_on_telemost(meet.room_uri)

    # Записали вчтречу и положили в файлик(soundcard/soundfile)
    audio(meet.room_uri)

    # Распознали текст из файла (openai/whisper-large-v3-turbo)
    text = speech(meet)

    # Подведение итогов встречи (ChatGPT/Llama)
    summary = processing(text)

    # Отправка итогов встерчи по почте (SMTPLib)
    send_email(summary, meet)

    meet.meet_finished = True
    meet.save()
