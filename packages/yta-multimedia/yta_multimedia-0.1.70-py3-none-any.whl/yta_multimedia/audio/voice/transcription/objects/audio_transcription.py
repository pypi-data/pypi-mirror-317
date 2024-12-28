from yta_multimedia.audio.voice.transcription.stt.whisper import WhisperTranscriptor
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.file.checker import FileValidator
from typing import Union


class AudioTranscriptionModel(Enum):
    """
    The different models/engines available to transcribe
    audios.
    """
    WHISPER_TIMESTAMPED = 'whisper_timestamped'

class AudioTranscription:
    """
    Class that represent an audio transcription, which
    is an audio that has been transcripted by using a
    AI transcription model.
    """
    _text: str = None
    """
    The whole text that has been transcripted, plain,
    as it is, as a string.
    """
    _words: list[dict] = None
    """
    An array containing each word that has been 
    transcripted, including the 'start' and 'end' time
    moments in which they have been said in the audio.
    """

    @property
    def text(self):
        """
        The whole text that has been transcripted, plain,
        as it is, as a string.
        """
        if self._text is None:
            self._text = ' '.join(self.words['text'])

        return self._text

    @property
    def words(self):
        """
        An array containing each word that has been 
        transcripted, including the 'start' and 'end' time
        moments in which they have been said in the audio.
        """
        return self._words

    def __init__(self, words: list[dict]):
        EXPECTED_FIELDS = ['text', 'start', 'end']
        if any(not all(field in word for field in EXPECTED_FIELDS) for word in words):
            raise ValueError(f'All words provided must have these fields: "{', '.join(EXPECTED_FIELDS)}"')

        self._words = words

    @staticmethod
    def transcribe(audio_filename: str, initial_prompt: Union[str, None] = None):
        """
        Transcribe the provided 'audio_filename' with the 
        default model and using the 'initial_prompt' as a
        help (if provided).

        The initial prompt will be sent to the model to
        improve the way it transcribes the audio. This,
        if we know the text that must be transcripted
        but we want to know the timing, could be a whole
        string containing the expected output text.
        """
        if not FileValidator.file_is_audio_file(audio_filename):
            raise Exception('The provided "audio_filename" is not a valid audio file.')
        
        # We use this model by default
        words, _ = WhisperTranscriptor.transcribe_with_timestamps(audio_filename, initial_prompt = initial_prompt)

        return AudioTranscription(words)