import os


def get_config(date):
    config = {}

    config['date'] = date  # '2024/08/18'
    config['voices_folder_prefix'] = f"PROCESSING/NICECXONE/MEDIA_PLAYBACK/VOICE/{config['date']}"
    config['transcripts_folder_prefix'] = f"PROCESSING/NICECXONE/MEDIA_PLAYBACK/VOICE/{config['date']}"
    config['insights_folder_prefix'] = f"PROCESSING/NICECXONE/MEDIA_PLAYBACK/INSIGHTS/{config['date']}"

    config['local_whisper_model'] = True
    # Options: {'openai_whisper' (not yet supported in Australia East as of Sep 2024), 'azure_stt': Azure Speech-to-Text model}
    config['azure_speech_model'] = 'azure_stt'

    config['insght_list'] = ['call_ID', 'main_reason_for_call', 'call_category', 'caller_type', 'received_information',
                             "Assess if the company representative in this conversation was consistently polite, caring, and actively trying to help, regardless of the customer's behavior."]

    return config
