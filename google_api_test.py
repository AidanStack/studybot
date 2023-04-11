import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech
import io

# Load environment variables from the .env file
load_dotenv()

# Get the path to the Google API credentials file from the environment variable
google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Load the credentials from the file
google_credentials = service_account.Credentials.from_service_account_file(
    google_credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

def transcribe_audio_file(file_path):
    client = speech.SpeechClient(credentials=google_credentials)

    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

file_path = "/Users/aidanstack/Documents/studybot/test_wav.wav"
transcribe_audio_file(file_path)
