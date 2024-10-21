import pandas as pd
from call_to_text_whisper import transcribe_whisper
from call_to_text_azure_stt import transcribe_az_sst

from insight_via_azureopenai import OpenAIInsight
from extract_load_azure_blob import AzureBlobAudioProcessor


class DailyInsights():
    def __init__(self, config):
        self.config = config
        self.ABAP = AzureBlobAudioProcessor(config)
        self.ABAP.login_to_azure()
        self.ABAP.initialize_blob_container()
        
    def get_calls_insight(self):
        insights_list = []
        blob_list = self.ABAP.get_list_of_calls()
        for blob in blob_list:
            if '.mp4' in blob.name:
                call_insights, transcript = self.get_one_call_insight(blob)
                insights_list.append(call_insights)
                transcript_path = self.config['transcripts_folder_prefix'] + blob.name + '.txt'
                self.ABAP.write_transcript(transcript, transcript_path)
                
        insight_path = self.config['insights_folder_prefix'] + 'insights.csv'    
        df = pd.DataFrame(insights_list, columns=self.config['insght_list'])
        self.ABAP.write_insight_csv(df, insight_path)

    def get_one_call_insight(self, blob):   
        audio_raw = self.ABAP.download_blob(blob)
        if audio_raw:
            OAII = OpenAIInsight(self.config)
            if audio_raw:
                audio = self.ABAP.get_normalized_audio_samples(audio_raw)

                if self.config['local_whisper_model']:
                    transcript = transcribe_whisper(audio)
                else:
                    transcript = transcribe_az_sst(self.config, audio)

                if not "Azure AI service failed".lower() in transcript.lower():
                    payload = OAII.make_payload(transcript)
                    response = OAII.send_payload_to_model(payload)
                    call_insights = OAII.postprocess_response(response, blob.name)
                    return call_insights, transcript
                else:
                    return [blob.name.split('.')[0]] + [transcript] * (len(self.config['insght_list']) - 1), transcript
            else:
                return None, None