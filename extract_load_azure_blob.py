import platform
import os
import subprocess
import numpy as np
from io import BytesIO, StringIO
from pydub import AudioSegment
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential


class AzureBlobAudioProcessor:
    def __init__(self, config):
        self.config = config
        self.account_url = os.getenv('AZURE_ACCOUTN_URL') 
        if not self.account_url: 
            raise Exception("Azure account url not set in environment variables")
        self.container_name = os.getenv('AZURE_CONTAINER_NAME')
        if not self.container_name:
            raise Exception('Azure container name not set in environment variables')
        self.voices_folder_prefix = config['voices_folder_prefix']
        self.container_client = None

    def login_to_azure(self):
        # Run the az login command using the username and password
        try:
            password = os.getenv('AZURE_USERNAME')
            if not password:
                raise Exception("Azure username not set in environment variables")
            
            password = os.getenv('AZURE_PASSWORD')
            if not password:
                raise Exception("Azure password not set in environment variables")

            # Define the Azure CLI command based on the OS and then use the standard 'az' command for Mac
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["az", "login", "--username", self.config['username'],
                                "--password", password], check=True)
            elif platform.system() == "Windows":  # Windows
                # Full path to az.cmd for Windows and then run the az login command using subprocess for Windows
                az_path = r'C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin\az.cmd'
                subprocess.run([az_path, "login", "--username", self.config['username'],
                                "--password", password], check=True)

            print(f"Login successful with account: {self.config['username']}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during login: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def initialize_blob_container(self):
        # Initializes the connection to the Azure Blob container.

        # Use the credentials from the CLI login
        credential = DefaultAzureCredential()

        # Access your Azure resources using the credentials
        blob_service_client = BlobServiceClient(
            account_url=self.account_url, credential=credential)
        self.container_client = blob_service_client.get_container_client(
            self.container_name)

    def get_list_of_calls(self):
        # blob_list = self.container_client.list_blobs(name_starts_with=self.voices_folder_prefix)
        blob_list = list(self.container_client.list_blobs(
            name_starts_with=self.voices_folder_prefix))

        for blob in blob_list:
            print(blob.name)
        return blob_list

    def download_blob(self, blob):
        blob_client = self.container_client.get_blob_client(blob.name)
        stream = BytesIO()
        blob_client.download_blob().readinto(stream)
        stream.seek(0)
        audio = AudioSegment.from_file(stream)
        return audio

    def get_normalized_audio_samples(self, audio):
        if self.config['local_whisper_model']:
            # Convert the audio to a NumPy array and normalize to [-1, 1] float32 that can be passed to whisper model
            samples = np.array(audio.get_array_of_samples()).astype(np.float32)
            samples /= np.max(np.abs(samples))  # Normalization
            return samples
        else:
            wav_io = BytesIO()
            audio.export(wav_io, format="wav")
            wav_io.seek(0)  # Reset the stream to the beginning
            return wav_io  # Return the WAV file as an in-memory stream

    def write_transcript(self, transcript, transcript_path):
        blob_client = self.container_client.get_blob_client(transcript_path)
        blob_client.upload_blob(transcript, overwrite=True)

    def write_insight_csv(self, df, csv_path):
        # Convert DataFrame to CSV in memory (using StringIO)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        # Get the blob client for the specific CSV file
        blob_client = self.container_client.get_blob_client(csv_path)
        # Upload the CSV content (StringIO is for text)
        blob_client.upload_blob(csv_buffer.getvalue(), overwrite=True)
