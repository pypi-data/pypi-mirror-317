from moviepy import AudioFileClip, concatenate_audioclips
from yta_multimedia.resources.audio.drive_urls import TYPING_KEYBOARD_3_SECONDS_GOOGLE_DRIVE_DOWNLOAD_URL
from yta_multimedia.audio.silences import AudioSilence
from yta_multimedia.video.edition.effect.constants import EFFECTS_RESOURCES_FOLDER
from yta_multimedia.resources import Resource
from typing import Union


class SoundGenerator:
    # TODO: Move this to a consts.py file
    TYPING_SOUND_FILENAME = EFFECTS_RESOURCES_FOLDER + 'sounds/typing_keyboard_3s.mp3'

    @classmethod
    def create_typing_audio(cls, output_filename: Union[str, None] = None):
        """
        Creates a typing audioclip of 3.5 seconds that, if 
        'output_filename' is provided, is stored locally
        with that name.
        """
        audio_filename = Resource.get(TYPING_KEYBOARD_3_SECONDS_GOOGLE_DRIVE_DOWNLOAD_URL, cls.TYPING_SOUND_FILENAME)
        audioclip = AudioFileClip(audio_filename)
        silence_audioclip = AudioSilence.create(0.5)

        audioclip = concatenate_audioclips([audioclip, silence_audioclip])

        if output_filename:
            # TODO: Validate 'output_filename'
            audioclip.write_audiofile(output_filename)

        return audioclip
