# call-center-insights-azure-ai

## Overview

This repository offers a Python-based solution for transcribing call conversations and extracting insights from recorded audio files stored in Azure Blob Storage. Given a **date** as input, the system retrieves the corresponding audio files from Azure, generates transcriptions, and extracts insights, saving them as a `.csv` file. These insights can be stored in cloud data warehouses like **Snowflake**, while both the `.txt` transcripts and `.csv` insights are stored in **Azure Blob Storage** for future reference.


## Features

- **Call to text**: Converts the call's recorded conversation into text using one of the supported speech-to-text models.
- **Multiple Speech-to-Text Model Options**:
  1. **Local Whisper Model**: A locally hosted Whisper model, ideal for free usage but slower when run on CPU.
  2. **Azure Speech-to-Text**: An Azure-hosted speech-to-text model that requires an API key and endpoint for use.
  3. **OpenAI Whisper Model**: Integrated with Azure AI services but currently not supported in the **Australia East** region as of September 2024.

### Key Details

- **Local Whisper Model**: Free, but performance is limited by CPU speed.
- **Azure Speech-to-Text**: Charged at $1.473 per hour for Real-time Transcription.
- **OpenAI Whisper Model**: Available for future use but currently not supported in Australia East.


- **Insight_via_azureopenai**: Extracts insights from the call transcript, represented as a list, which can be appended to an existing table in Snowflake for further analysis.

## Workflow


1. A date in the format YYYY/MM/DD is provided as input to the code.
2. All conversation audio files stored in the corresponding directory for that date are iterated over.
3. Each audio file is processed by a speech-to-text model, and the resulting transcript is passed to Azure OpenAI, where insights are extracted using a GPT-4 model for deeper analysis.
4. The resulting transcripts are saved in the TRANSCRIPTS folder on Azure Blob Storage.
5. The extracted insights are stored in a .csv file in the corresponding INSIGHTS folder on Azure Blob Storage.



## Prerequisites

- Python 3.x installed on your local system.
- A Snowflake account and access to the relevant database.
- An Azure account with access to Azure Blob Storage and Speech-to-Text services.
- **Local Whisper Model** setup if using the local model for transcription.

## Setup and Installation

1. **Clone the repository**:
2. Install dependencies: Install the required libraries listed in requirements.txt: `pip install -r requirements.txt`  
Note: `ffmpeg` must be installed separately.
3. Configure Credentials:

Set up your user credentials in the configuration file (`configuration.py`).
For storing sensitive information follow these instructions:  
sensetive intformatiob (AZURE_ACCOUTN_URL, AZURE_CONTAINER_NAME, AZURE_USERNAME, AZURE_PASSWORD, Azure_OpenaAI_key, azure_speach_to_text_api_key (if needed))

- **Mac/Linux**: Store environment variables in `~/.bash_profile`.
- **Windows**: Use the **Environment Variables** section in the system settings.

4.  Set up the Speech-to-Text Model in configuration (config['azure_speech_model'])
(Ensure the appropriate API keys and endpoints are provided for Azure models.)

## Running the Code
5. Run the script: `python main.py <date>`
The script will process the audio, extract insights, and returns botht the insight and the transcript  respectively.
