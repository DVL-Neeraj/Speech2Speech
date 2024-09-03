import json
import os
from dotenv import load_dotenv

from ibm_watsonx_ai import Credentials

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watson import SpeechToTextV1
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from speechtotext import load_speech2text_credentials,speech_to_text
from text_translator import load_credentials_text_translator,load_model,text_translator
from text2speech import load_credentials_text2speech, text_to_audio

model_name= "de-DE_NarrowbandModel"
file_path = 'health-german.mp3'
file_name = file_path.split('.')[0]

def main(file_path):
    #loading the speech2text output
    speech_to_text_model = load_speech2text_credentials()
    print('speech2text model loaded.')
    transcript_json = speech_to_text(file_path,model_name,speech_to_text_model)
    print('transcript_json loaded.')

    #loading text translator output
    credentials, project_id = load_credentials_text_translator()
    print('credentials, project_id loaded.')
    model = load_model(credentials,project_id)
    print('translator model loaded.')

    translated_json = text_translator(model,transcript_json)
    print('translated_json loaded.')

    #loading text to audio output:
    text_to_speech_model = load_credentials_text2speech()
    print('text_to_speech_model loaded.')
    return text_to_audio(translated_json,text_to_speech_model)

main(file_path=file_path)