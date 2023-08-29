import os
from dotenv import load_dotenv

from sqlalchemy.orm import Session
import json

# langchain imports
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain.output_parsers import PydanticOutputParser

from botocore.exceptions import ClientError
from pydub import AudioSegment
import boto3
from xml.sax.saxutils import escape
import io


# local imports
from . import models

load_dotenv()


class LifeCoach:
    client_name: str
    coach_info: str = "You are a life coach"
    query: str
    db: Session
    mindstate: str
    voice: str = "Emma"
    voice_speed: int = 100

    def __init__(
        self,
        user_id: int,
        coach_info: str,
        db: Session,
    ) -> None:
        # get username
        user = db.query(models.Users).filter(models.Users.id == user_id).first()
        if not user:
            raise Exception(f"Error, no user found for user_id: {user_id}")
        self.client_name = user.name

        # get mindstate
        mind_state = (
            db.query(models.MindState)
            .filter(models.MindState.user_id == user_id)
            .first()
        )
        if not mind_state:
            return json.dumps({"error": "MindState not found"})

        # Prepare the data for JSON
        data = {"user": user.name, "MindState": {}}

        for column in models.MindState.__table__.columns:
            col_name = column.name.replace("_", " ")
            col_value = getattr(mind_state, column.name)
            if col_value:
                data["MindState"][col_name] = col_value

        self.user_mindstate = json.dumps(data)
        self.coach_info = coach_info

    def create_exercise_text(self, query: str) -> str:
        # create system prompt
        prompt = PromptTemplate(
            template="""{coach_info}. You will be asked to create exercises for the user, based only on the information provided below in JSON. Use their name ({name}) in the exercises.  \n\n
                        {mindstate}""",
            input_variables=["coach_info", "name", "mindstate"],
        )
        # add supplied variables
        formatted_message = prompt.format_prompt(
            coach_info=self.coach_info, name=self.client_name, mindstate=self.mindstate
        )

        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7, max_tokens=1024)

        messages = [
            SystemMessage(content=str(formatted_message)),
            HumanMessage(content=query),
        ]

        return llm(messages)

    def create_exercise_speech(self, query: str):
        text = self.create_exercise_text(query)
        # polly code here
        # Maximum character limit for Polly
        MAX_CHAR_LIMIT = 3000

        # Split the text into parts if it exceeds the character limit
        text_parts = [
            text[i : i + MAX_CHAR_LIMIT] for i in range(0, len(text), MAX_CHAR_LIMIT)
        ]

        combined_audio = AudioSegment.empty()

        for part in text_parts:
            # Sanitize the text by escaping special XML characters
            sanitized_part = escape(part, {"'": "&apos;", '"': "&quot;"})

            # Wrap the sanitized text in SSML with a prosody tag to set the rate
            ssml_part = f"<speak><prosody rate='{self.voice_speed}%'>{sanitized_part}</prosody></speak>"

            # Create a Polly client
            polly_client = boto3.Session(
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name="ap-southeast-1",
            ).client("polly")

            try:
                # Request speech synthesis using SSML
                response = polly_client.synthesize_speech(
                    Text=ssml_part,
                    OutputFormat="mp3",
                    VoiceId=self.voice,
                    TextType="ssml",  # Set the text type to SSML
                    Engine="neural",
                    LanguageCode="en-GB",
                )
            except ClientError as e:
                http_status_code = e.response["ResponseMetadata"]["HTTPStatusCode"]
                aws_error_code = e.response["Error"]["Code"]
                error_message = f"Failed to synthesize speech using Amazon Polly. HTTP status code: {http_status_code}, AWS error code: {aws_error_code}"
                raise RuntimeError(error_message) from e

            # Read the audio data and create an AudioSegment object
            audio_data = response["AudioStream"].read()
            audio_segment = AudioSegment.from_mp3(io.BytesIO(audio_data))

            # Append this segment to the combined audio
            combined_audio += audio_segment

        # Save the combined audio to a file
        # construct the file path using user_id
        file_path = os.path.join("audio", str(self.user_id), "temp.mp3")
        # create directory if it does not exist
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        # Save the combined audio to the file
        combined_audio.export(file_path, format="mp3")

        return file_path
