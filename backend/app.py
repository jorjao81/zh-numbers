# Main Flask application file
from flask import Flask, jsonify, request, render_template
import os
import random
from number_converter import to_chinese_numeral
from dotenv import load_dotenv
import io
from pydub import AudioSegment

# Azure Speech SDK
import azure.cognitiveservices.speech as speechsdk

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Configure Azure Speech credentials
SPEECH_KEY = os.environ.get('SPEECH_KEY')
SPEECH_REGION = os.environ.get('SPEECH_REGION')

if not SPEECH_KEY or not SPEECH_REGION:
    raise RuntimeError("SPEECH_KEY and SPEECH_REGION must be set in the environment.")

speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
# The language for pronunciation assessment.
# The format is BCP-47 language tag.
# See more information at: https://learn.microsoft.com/azure/ai-services/speech-service/language-support?tabs=stt
speech_config.speech_recognition_language = "zh-CN"


@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/api/number', methods=['GET'])
def get_number():
    """Returns a random number (1-999) and its Chinese representation."""
    number = random.randint(1, 999)
    try:
        chinese_numeral = to_chinese_numeral(number)
        return jsonify({"number": number, "chinese": chinese_numeral})
    except ValueError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/pronounce', methods=['POST'])
def pronounce():
    """Receives audio and reference text, and returns pronunciation assessment."""
    audio_file = request.files.get('audio')
    reference_text = request.form.get('chinese')

    if not audio_file or not reference_text:
        return jsonify({"error": "Missing audio file or reference text"}), 400

    # The audio from the browser is in webm format. The Azure SDK needs WAV format.
    # We use pydub to convert the audio in-memory.
    try:
        audio_data = audio_file.read()
        # Load webm audio from bytes
        webm_audio = AudioSegment.from_file(io.BytesIO(audio_data), format="webm")

        # The Azure SDK wants WAV with specific properties.
        # 16kHz, 16-bit, single-channel
        wav_audio = webm_audio.set_frame_rate(16000).set_sample_width(2).set_channels(1)

        # Export to an in-memory WAV file
        wav_buffer = io.BytesIO()
        wav_audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)

    except Exception as e:
        return jsonify({"error": f"Audio conversion failed: {str(e)}"}), 500


    # The Azure SDK requires audio data to be pushed into a stream.
    # We push the converted WAV data into the stream.
    push_stream = speechsdk.audio.PushAudioInputStream()
    push_stream.write(wav_buffer.read())
    push_stream.close()

    audio_config = speechsdk.audio.AudioConfig(stream=push_stream)

    # Create pronunciation assessment config
    pronunciation_config = speechsdk.PronunciationAssessmentConfig(
        reference_text=reference_text,
        grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
        granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
        enable_miscue="True"
    )

    # Create a speech recognizer
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    pronunciation_config.apply_to(recognizer)

    # Start recognition
    result = recognizer.recognize_once()

    # Process the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        pronunciation_result = speechsdk.PronunciationAssessmentResult(result)
        return jsonify({
            "accuracyScore": pronunciation_result.accuracy_score,
            "fluencyScore": pronunciation_result.fluency_score,
            "completenessScore": pronunciation_result.completeness_score,
            "pronunciationScore": pronunciation_result.pronunciation_score,
            "errorType": "None" # Placeholder, can be enhanced with word-level feedback
        })
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return jsonify({"error": "Speech could not be recognized."}), 500
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return jsonify({
            "error": f"Speech Recognition canceled: {cancellation_details.reason}",
            "details": str(cancellation_details.error_details)
        }), 500
    else:
        return jsonify({"error": "An unknown error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
