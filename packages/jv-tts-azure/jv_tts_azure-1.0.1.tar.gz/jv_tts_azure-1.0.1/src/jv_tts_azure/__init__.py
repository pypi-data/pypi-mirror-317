from jvcore import TextToSpeech
from .azure_tts import AzureTextToSpeech

def getTts() -> TextToSpeech:
    return AzureTextToSpeech()