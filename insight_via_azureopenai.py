import os
import json
import time
import requests


class OpenAIInsight:
    def __init__(self, config):
        self.config = config

    def make_payload(self, voice_text):
        # Payload for the request
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are an AI assistant tasked with analyzing a transcript extracted from recorded conversations in a call center, potentially impacted by poor voice-to-text translation quality. Your objective is to extract evidence-based insights from the content of these conversations. Ensure that all insights are directly supported by the transcript, avoiding any assumptions or speculative conclusions."
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please provide the insights in the following JSON format:\n{\n    \"main_reason_for_call\": \"string\",\n    \"call_category\": \"one of [Test Result Inquiries, Lab Order Modifications, Test Clarifications, Appointments and Scheduling, Logistics, Miscellaneous, Non recognizable]\",\n    \"caller_type\": \"patient or clinic representative\",\n    \"received_information\": \"yes or no\",\n    \"Assess if the pathology representative in this conversation was consistently polite, caring, and actively trying to help, regardless of the customer's behavior.\": \"positive or negative\"\n}\n\nOnly provide the JSON object as the output, without any additional text."
                        },
                        {
                            "type": "text",
                            "text": f"Here is the transcript:\n\n{voice_text}"
                        }
                    ]
                }
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 800
        }

        return payload

    def send_payload_to_model(self, payload, max_retries=5):
        API_KEY = os.getenv('Azure_OpenaAI_key')
        if not API_KEY:
            raise Exception(
                "Azure_OpenaAI_key not set in environment variables")

        headers = {
            "Content-Type": "application/json",
            "api-key": API_KEY,
        }
        ENDPOINT = "https://call-center-poc0.openai.azure.com/openai/deployments/text-insight-poc0/chat/completions?api-version=2024-02-15-preview"

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    ENDPOINT, headers=headers, json=payload)
                response.raise_for_status()  # Ensure it was successful
                response_json = response.json()
                insights = response_json['choices'][0]['message']['content']
                return insights  # Return the result
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    retry_after = int(response.headers.get(
                        "Retry-After", 2 ** attempt))
                    print(
                        f"Rate limit exceeded, retrying after {retry_after} seconds...")
                    time.sleep(retry_after)
                elif response.status_code == 400:
                    return "Failed to make the request: Bad Request (400)"
            except Exception as e:
                return f"Failed to make the request: Error: {e}"

        # After all retries fail, return this
        return f"Failed to make the request: Rate limit exceeded"

    def cleanup_Category(self, category):
        predefined_Categories = ['Test Result Inquiries', 'Lab Order Modifications', 'Test Clarifications',
                                 'Appointments and Scheduling', 'Logistics', 'Miscellaneous', 'Non recognisable']
        for item in predefined_Categories:
            if item.lower() in category.lower():
                return item
        return 'Category Not found'

    def postprocess_response(self, response, call_id):
        if "Failed to make the request" in response:
            stripped_response = response.split(
                'Failed to make the request: ')[1].strip()
            new_row = [call_id.split('.')[0]] + [stripped_response] * \
                (len(self.config['insght_list']) - 1)
        else:
            # Extract the JSON-like part of the response
            stripped_response = '{' + response.strip().split('{', 1)[1]
            insight_string = stripped_response.rstrip('```').strip()

            # Convert to JSON and add as a new row
            insights_dict = json.loads(insight_string)
            new_row = [call_id.split('.')[0]] + list(insights_dict.values())
            new_row[2] = self.cleanup_Category(new_row[2])
        return new_row
