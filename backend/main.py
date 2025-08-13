from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, File, Form
from pathlib import Path
import random
import os
from tempfile import NamedTemporaryFile
import azure.cognitiveservices.speech as speechsdk

app = FastAPI()
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
DIGITS = "零一二三四五六七八九"

def number_to_chinese(n: int) -> str:
    if n == 0:
        return DIGITS[0]
    units = [1000, 100, 10, 1]
    unit_chars = ["千", "百", "十", ""]
    result = ""
    zero_flag = False
    for unit, ch in zip(units, unit_chars):
        digit = n // unit
        n %= unit
        if digit == 0:
            if result:
                zero_flag = True
        else:
            if zero_flag:
                result += DIGITS[0]
                zero_flag = False
            if unit == 10 and digit == 1 and result == "":
                result += ch
            else:
                result += DIGITS[digit] + ch
    return result

@app.get("/api/number")
async def get_number():
    number = random.randint(0, 9999)
    return {"number": number, "text": number_to_chinese(number)}

@app.post("/api/assess")
async def assess_pronunciation(number: int = Form(...), audio: UploadFile = File(...)):
    reference_text = number_to_chinese(number)
    contents = await audio.read()
    with NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name
    try:
        speech_key = os.environ["AZURE_SPEECH_KEY"]
        speech_region = os.environ["AZURE_SPEECH_REGION"]
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        audio_config = speechsdk.audio.AudioConfig(filename=tmp_path)
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config, language="zh-CN")
        pron_config = speechsdk.PronunciationAssessmentConfig(reference_text=reference_text)
        pron_config.apply_to(recognizer)
        result = recognizer.recognize_once_async().get()
        assessment = speechsdk.PronunciationAssessmentResult(result)
        return {
            "reference": reference_text,
            "accuracy": assessment.accuracy_score,
            "pronunciation": assessment.pronunciation_score,
            "completeness": assessment.completeness_score,
            "fluency": assessment.fluency_score,
        }
    finally:
        os.remove(tmp_path)
