import os
import requests


def send_audio_to_azure(audio_stream, subscription_key, region, model):
    if (model == 'azure_stt'):
        # Define Azure Speech-to-Text endpoint
        endpoint = f"https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"

        # Headers required for the API call
        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type': 'audio/wav',  # WAV audio format
            'Accept': 'application/json',
        }

        # Parameters (set language)
        params = {
            'language': 'en-AU',  # Set the language
        }

    elif model == 'openai_whisper':
        # Define OpenAI Whisper endpoint (replace with your actual endpoint)
        endpoint = "https://call-center-poc-whisper.openai.azure.com/openai/deployments/whisper/models/whisper/transcriptions"

        # Headers required for the API call
        headers = {
            'api-key': subscription_key,  # Use the API key for authentication
            'Content-Type': 'audio/wav',  # WAV audio format
            'Accept': 'application/json',
        }

        # Your parameters for the Whisper model (if any, based on your specific deployment)
        params = {
            'language': 'en-AU',  # Set to Australian English
            'profanityFilter': True,  # Optional: enable or disable profanity filtering
        }

    try:
        # Send the audio to the OpenAI Whisper API
        response = requests.post(
            endpoint, headers=headers, params=params, data=audio_stream)

        # Check response and print transcription
        if response.status_code == 200:
            return response.json()['DisplayText']
        else:
            return f"Azure AI service failed: {response.status_code}"

    except Exception as e:
        return (f"Azure AI service failed: {e}")


def transcribe_az_sst(config, wav_stream):
    subscription_key = os.getenv('azure_speach_to_text_api_key')
    region = 'australiaeast'
    transcript = send_audio_to_azure(
        wav_stream, subscription_key, region, config['azure_speech_model'])
    return transcript
