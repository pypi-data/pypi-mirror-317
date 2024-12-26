from jvcore import SpeechToText
from .azure_stt import AzureSpeechToText

def getStt() -> SpeechToText:
    return AzureSpeechToText()