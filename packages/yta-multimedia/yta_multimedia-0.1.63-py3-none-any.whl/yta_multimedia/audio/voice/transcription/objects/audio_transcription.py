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
    _audio_filename: str = None
    _model: AudioTranscriptionModel = None
    _initial_prompt: str = None
    """
    This is the prompt we will send to the model to
    improve the way it transcribes the audio. This,
    if we know the text that must be transcripted
    but we want to know the timing, could be a whole
    string containing the expected output text.
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
            self._transcribe()

        return self._text

    @property
    def words(self):
        """
        An array containing each word that has been 
        transcripted, including the 'start' and 'end' time
        moments in which they have been said in the audio.
        """
        if self._words is None:
            self._transcribe()

        return self._words

    def __init__(self, audio_filename: str, model: AudioTranscriptionModel = AudioTranscriptionModel.WHISPER_TIMESTAMPED, initial_prompt: Union[str, None] = None):
        if not FileValidator.file_is_audio_file(audio_filename):
            raise Exception('The provided "audio_filename" is not a valid audio file.')
        
        self._audio_filename = audio_filename
        self._initial_prompt = initial_prompt
        self._model = AudioTranscriptionModel.to_enum(model)

    def _transcribe(self, do_force: bool = False):
        """
        Transcribe the audio and obtain the text and 
        words transcripted with their timestamps.
        """
        if do_force or (self._words is None or self._text is None):
            if self._model == AudioTranscriptionModel.WHISPER_TIMESTAMPED:
                words, text = WhisperTranscriptor.transcribe_with_timestamps(self._audio_filename, initial_prompt = self._initial_prompt)

            self._words = words
            self._text = text