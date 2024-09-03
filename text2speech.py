from dotenv import load_dotenv
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
import json


def load_credentials_text2speech():
    load_dotenv()
    api_key = os.getenv('Watsonx_text2speech_api_key') 


    authenticator = IAMAuthenticator(api_key)
    text_to_speech_model = TextToSpeechV1(
        authenticator=authenticator
    )

    text_to_speech_model.set_service_url('https://api.jp-tok.text-to-speech.watson.cloud.ibm.com/instances/dde47a40-dc24-494e-9e98-83e327f51b00')
    return text_to_speech_model

#voices = text_to_speech.list_voices().get_result()
#print(json.dumps(voices, indent=2))

#file_path = 'translated_text/translated_text.json'

def text_to_audio(file_path,text_to_speech_model):
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    input_text = data['translated_text']
    audio_name = file_path.split('/')[-1].replace(".json",".mp3")

    with open(f"translated_audio/{audio_name}", 'wb') as audio_file:
        audio_file.write(
            text_to_speech_model.synthesize(
                input_text,
                voice='en-US_AllisonV3Voice',
                accept='audio/mp3'        
            ).get_result().content)
        print('Done! Audio Converted!')
