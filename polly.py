from xml.sax.saxutils import escape
from botocore.exceptions import ClientError
from pydub import AudioSegment
import boto3
import os
import io

def text_to_speech(text, file_name, speed=100, voice="Emma"):

    # Maximum character limit for Polly
    MAX_CHAR_LIMIT = 3000

    # Split the text into parts if it exceeds the character limit
    text_parts = [text[i:i+MAX_CHAR_LIMIT] for i in range(0, len(text), MAX_CHAR_LIMIT)]
    
    combined_audio = AudioSegment.empty()

    for part in text_parts:
        # Sanitize the text by escaping special XML characters
        sanitized_part = escape(part, {"'": "&apos;", '"': "&quot;"})

        # Wrap the sanitized text in SSML with a prosody tag to set the rate
        ssml_part = f"<speak><prosody rate='{speed}%'>{sanitized_part}</prosody></speak>"

        # Create a Polly client
        polly_client = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name='ap-southeast-1').client('polly')

        try:
            # Request speech synthesis using SSML
            response = polly_client.synthesize_speech(
                Text=ssml_part,
                OutputFormat='mp3',
                VoiceId=voice,
                TextType='ssml',  # Set the text type to SSML
                Engine="neural",
                LanguageCode="en-GB"
            )
        except ClientError as e:
            http_status_code = e.response['ResponseMetadata']['HTTPStatusCode']
            aws_error_code = e.response['Error']['Code']
            error_message = f"Failed to synthesize speech using Amazon Polly. HTTP status code: {http_status_code}, AWS error code: {aws_error_code}"
            raise RuntimeError(error_message) from e

        # Read the audio data and create an AudioSegment object
        audio_data = response['AudioStream'].read()
        audio_segment = AudioSegment.from_mp3(io.BytesIO(audio_data))

        # Append this segment to the combined audio
        combined_audio += audio_segment

    # Save the combined audio to a file
    final_audio_path = file_name + '.mp3'
    combined_audio.export(final_audio_path, format='mp3')

    return final_audio_path
