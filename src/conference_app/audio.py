from  datetime import *
import soundcard as sc
import soundfile as sf
from src.creds import TMP_PATH
from src.database.SQl.database_controller import Meets


def audio():
    """Запись аудио онлайн конференции в файл"""
    for meet in Meets.select():

        output_file_name = f'{TMP_PATH}/{meet.room_uri[21:]}.mp3'  # file name.
        sample_rate = 48000  # [Hz]. sampling rate.
        time_difference = meet.end_meet_date - datetime.now().replace(microsecond=0)
        record_sec = time_difference.total_seconds() # [sec]. duration recording audio.

        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(
                samplerate=sample_rate) as mic:
            # record audio with loopback from default speaker.
            data = mic.record(numframes=sample_rate * record_sec)

            # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
            print('Аудио запись успешно сохранено в файл.')
            sf.write(file=output_file_name, data=data[:, 0], samplerate=sample_rate)

        meet.file = "success True"
        meet.save()
