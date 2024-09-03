from ibm_watsonx_ai import Credentials
import json
import os
from dotenv import load_dotenv

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from ibm_watsonx_ai.foundation_models import ModelInference



def load_credentials_text_translator():
    load_dotenv()

    project_id = os.getenv('project_id')
    #print(project_id)
    model_api_key = os.getenv('Watsonx_models_api_key')
    #print(model_api_key)

    credentials = Credentials(
        url="https://jp-tok.ml.cloud.ibm.com",
        api_key=model_api_key)
    print('Credentials for text translation loaded!')
    return credentials, project_id


def load_model(credentials,project_id):
    model_id = "ibm/granite-20b-multilingual"

    parameters = {
        GenParams.DECODING_METHOD: DecodingMethods.SAMPLE,
        GenParams.MAX_NEW_TOKENS: 1000,
        GenParams.MIN_NEW_TOKENS: 1,
        GenParams.TEMPERATURE: 0.1,
        GenParams.TOP_K: 50,
        GenParams.TOP_P: 1,
        GenParams.STOP_SEQUENCES: ["/n"]
    }

    model = ModelInference(
        model_id=model_id, 
        params=parameters, 
        credentials=credentials,
        project_id=project_id)
    
    print('Text translation model loaded.')
    return model


def text_translator(model,file_path):
    #file_path = 'transcripts/health-german..json'
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    input_text = data['transcript']

    german_to_english_query1 = f"""Translate the following text from German to English:

    Input: {input_text}
    Output:
    """
    #print(german_to_english_query)

    translation_result = model.generate_text(german_to_english_query1)

    print('translation_result:',translation_result)

    translated_text = {'translated_text':translation_result}
    file_name = file_path.split('/')[-1]
    json_path = f'translated_text/{file_name}'

    with open(json_path, "w",encoding="utf-8") as json_file:
        json.dump(translated_text, json_file, indent=2,ensure_ascii=False)
    print('Done!')
    return json_path