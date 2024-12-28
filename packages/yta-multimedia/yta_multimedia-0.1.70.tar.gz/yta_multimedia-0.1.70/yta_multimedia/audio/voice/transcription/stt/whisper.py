from yta_general_utils.file.checker import FileValidator
from yta_general_utils.programming.enum import YTAEnum as Enum
from typing import Union

import whisper_timestamped


def get_transcription_text(audio_filename, model = 'base'):
    """
    Receives an 'audio_filename' and gets the transcription of it,
    returning only the text. This is a simple and faster method
    to be used when we simply want the text without timestamps.
    """
    from faster_whisper import WhisperModel
    # TODO: What if 'whisper_timestamped' is better? We should use it

    model = WhisperModel(model)

    segments, _ = model.transcribe(audio_filename, language = 'es', beam_size = 5)

    text = ""
    for segment in segments:
        text += segment.text + ' '

    text = text.strip()

    return text

# Very interesting (https://github.com/m-bain/whisperX) to get timestamps of each word
# But the one I use is this one (https://github.com/linto-ai/whisper-timestamped)
def get_transcription_with_timestamps(audio_filename, model = 'small', initial_prompt = None):
    """
    Receives an 'audio_filename' and makes a transcription of it, returning a 
    list of 'segments' in the result. You can pass an 'initial_prompt' to help
    the model to recognize some specific words and to have a better performance.

    This method returns a list of the words recognized in the audio with the
    next parameters: 'text' (word string), 'start' (the moment in which that
    word starts being dictated in the audio), 'end' (the moment in which the 
    word stops being dictated in the audio) and 'confidende' (the certainty
    with which the model has recognize that word, from 0 to 1).
    """
    audio = whisper_timestamped.load_audio(audio_filename)
    model = whisper_timestamped.load_model(model, device = "cpu")
    
    # I do this 'initial_prompt' formatting due to some issues when using it 
    # as it was. I read in Cookguide to pass natural sentences like this below
    # and it seems to be working well, so here it is:
    if initial_prompt != None:
        #initial_prompt = '""""' + initial_prompt + '""""'
        #initial_prompt = 'I know exactly what is said in this audio and I will give it to you (between double quotes) to give me the exact transcription. The audio says, exactly """"' + initial_prompt + '""""'
        initial_prompt = 'I will give you exactly what the audio says (the output), so please ensure it fits. The output must be """"' + initial_prompt + '""""'

    # 'vad' = True would remove silent parts to decrease hallucinations
    # 'detect_disfluences' detects corrections, repetitions, etc. so the
    # word prediction should be more accurate. Useful for natural narrations
    result = whisper_timestamped.transcribe(model, audio, language = "es", initial_prompt = initial_prompt)
    
    return result

# TODO: Check all above because it can be deleted
# or refactored, but not by now, need to review it
# carefully
class WhisperModel(Enum):
    """
    The model of Whisper you want to use to detect
    the audio.

    See more:
    https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages
    """
    TINY = 'tiny'
    """
    Trained with 39M parameters.
    Required VRAM: ~1GB.
    Relative speed: ~10x.
    """
    BASE = 'base'
    """
    Trained with 74M parameters.
    Required VRAM: ~1GB.
    Relative speed: ~7x.
    """
    SMALL = 'small'
    """
    Trained with 244M parameters.
    Required VRAM: ~2GB.
    Relative speed: ~4x.
    """
    MEDIUM = 'medium'
    """
    Trained with 769M parameters.
    Required VRAM: ~5GB.
    Relative speed: ~2x.
    """
    LARGE = 'large'
    """
    Trained with 1550M parameters.
    Required VRAM: ~10GB.
    Relative speed: ~1x.
    """
    TURBO = 'turbo'
    """
    Trained with 809M parameters.
    Required VRAM: ~6GB.
    Relative speed: ~8x.
    """
class WhisperTranscriptor:
    """
    An audio transcriptor based on the Whisper
    model that is capable of transcribing audios
    giving the start and end time of each word
    said in the audio.
    """
    @staticmethod
    def transcribe_with_timestamps(audio_filename: str, model: WhisperModel = WhisperModel.SMALL, initial_prompt: Union[str, None] = None):
        """
        Transcribe the provided 'audio_filename' using the
        specified 'model' and obtains a list of 'words' (with
        the 'start' and 'end' times) and the whole 'text' in
        the audio.

        This method returns the tuple (words, text).
        """
        if not FileValidator.file_is_audio_file(audio_filename):
            raise Exception('The provided "audio_filename" is not a valid audio file.')
        
        model = WhisperModel.to_enum(model)

        audio = whisper_timestamped.load_audio(audio_filename)
        model = whisper_timestamped.load_model(model.value, device = 'cpu')

        # See this: https://github.com/openai/openai-cookbook/blob/main/examples/Whisper_prompting_guide.ipynb
        # I do this 'initial_prompt' formatting due to some issues when using it 
        # as it was. I read in Cookguide to pass natural sentences like this below
        # and it seems to be working well, so here it is:
        if initial_prompt is not None:
            #initial_prompt = '""""' + initial_prompt + '""""'
            #initial_prompt = 'I know exactly what is said in this audio and I will give it to you (between double quotes) to give me the exact transcription. The audio says, exactly """"' + initial_prompt + '""""'
            initial_prompt = 'I will give you exactly what the audio says (the output), so please ensure it fits. The output must be """"' + initial_prompt + '""""'

        # 'vad' = True would remove silent parts to decrease hallucinations
        # 'detect_disfluences' detects corrections, repetitions, etc. so the
        # word prediction should be more accurate. Useful for natural narrations
        transcription = whisper_timestamped.transcribe(model, audio, language = "es", initial_prompt = initial_prompt)
        """
        'text', which includes the whole text
        'segments', which has the different segments
            'words', inside 'segments', which contains each 
            word and its 'text', 'start' and 'end'
        """
        words = [word for segment in transcription['segments'] for word in segment['words']]
        text = ' '.join([word['text'] for word in words])

        return words, text

        words = []
        text = ''
        for segment in transcription['segments']:
            for word in segment['words']:
                word.append(word)
                text += f'{word["text"]} '
        text = text.strip()

        return words, text

        
