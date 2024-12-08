import soundcard as sc
import soundfile as sf
from src.creds import TMP_PATH


def audio(meet_room_uri):
    """Запись аудио онлайн конференции в файл"""

    output_file_name = f'{TMP_PATH}/{meet_room_uri[21:]}.mp3'  # file name.
    sample_rate = 48000  # [Hz]. sampling rate.
    record_sec = 10  # [sec]. duration recording audio.

    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(
            samplerate=sample_rate) as mic:
        # record audio with loopback from default speaker.
        data = mic.record(numframes=sample_rate * record_sec)

        # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
        sf.write(file=output_file_name, data=data[:, 0], samplerate=sample_rate)
