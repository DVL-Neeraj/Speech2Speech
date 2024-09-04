from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from werkzeug.utils import secure_filename

from speechtotext import load_speech2text_credentials, speech_to_text
from text_translator import load_credentials_text_translator, load_model, text_translator
from text2speech import load_credentials_text2speech, text_to_audio

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/audio/'
# Create the upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            output_audio = process_audio(file_path)
            return send_file(output_audio, as_attachment=True,download_name=filename)

    return render_template('index.html')

def process_audio(file_path, model_name="de-DE_NarrowbandModel"):
    try:
        # Step 1: Speech-to-Text
        speech_to_text_model = load_speech2text_credentials()
        transcript_json = speech_to_text(file_path, model_name, speech_to_text_model)

        # Step 2: Text Translation
        credentials, project_id = load_credentials_text_translator()
        model = load_model(credentials, project_id)
        translated_json = text_translator(model, transcript_json)

        # Step 3: Text-to-Speech
        text_to_speech_model = load_credentials_text2speech()
        audio_output = text_to_audio(translated_json, text_to_speech_model)

        return audio_output

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    app.run(debug=True)
