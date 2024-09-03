#connecting the speech to text service:
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import os
from dotenv import load_dotenv

def load_speech2text_credentials():
    load_dotenv()

    api_key = os.getenv('Watsonx_api')

    authenticator = IAMAuthenticator(api_key)

    speech_to_text_model = SpeechToTextV1(
        authenticator=authenticator
    )

    speech_to_text_model.set_service_url('https://api.jp-tok.speech-to-text.watson.cloud.ibm.com/instances/b430d8ca-eb26-4f91-983e-979c329563ec')

    print('speech2text authenticated.')
    return speech_to_text_model

#model = speech_to_text.get_model(model_name)
#print(json.dumps(model, indent=2))

file_path = 'health-german.mp3'

def speech_to_text(file_path,model_name,speech_to_text_model):
    with open(file_path,'rb') as audio_file:
        response = speech_to_text_model.recognize(audio=audio_file, content_type='audio/mp3',model=model_name)
        #output = response.result['results'][0]['alternatives'][0]['transcript']
        output = response.result['results']
        text = ''
        for i in range(len(output)):
            text += output[i]['alternatives'][0]['transcript']

    transcription = {'transcript':text}
    file_name = file_path.split('/')[-1].replace('.mp3','')
    json_path = f'transcripts/{file_name}.json'
    with open(json_path, "w",encoding="utf-8") as json_file:
        json.dump(transcription, json_file, indent=2,ensure_ascii=False)
    print('Json stored!')
    return json_path

#speech_to_text_model = load_speech2text_credentials()
#speech_to_text(file_path,model_name,speech_to_text_model)