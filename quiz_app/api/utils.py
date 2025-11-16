import os

import yt_dlp
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

CLIENT = genai.Client(api_key=API_KEY)


class AudioQuestionGenerator:
    """
    Utility class to generate quiz questions
    from a YouTube audio track.

    Workflow:
        1. Download audio from a YouTube URL and convert to WAV.
        2. Transcribe the audio using OpenAI Whisper.
        3. Generate 10 multiple-choice quiz questions from the transcript
           using Gemini AI, strictly in JSON format.
        4. Clean and save generated quiz text to file.

    Attributes:
        - audio_track (str): Local filename of the downloaded audio.
        - transcribed_text (str): Local filename of the transcribed text.
        - generated_text (str): Local filename of the generated quiz content.

    Methods:
        - download_audio(url): Downloads and converts YouTube audio to WAV.
        - transcribe_whisper(): Transcribes audio into text using Whisper.
        - generate_questions_gemini(): Generates a quiz JSON
                                       from the transcript.
        - edge_cleaner_text(): Cleans formatting of generated quiz text.
        - remove_markdown(content): Removes markdown wrappers from text.
        - read_file(filename): Reads text content from a file.
        - write_file(filename, content): Writes text content to a file.
        - delete_transcribed_text(): Deletes the transcribed text file.
        - delete_generated_text(): Deletes the generated quiz text file.
    """

    audio_track = "audio_track"
    transcribed_text = "transcribed_text"
    generated_text = "generated_text"

    def download_audio(self, url):
        output_path = "media"
        os.makedirs(output_path, exist_ok=True)

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(output_path, "audio_track"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "0",
                }
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as audio:
            audio.extract_info(url, download=True)
            self.audio_track = "audio_track"

    def transcribe_whisper(self):
        import whisper 
        model = whisper.load_model("small", device="cpu")
        audio_file = f"media/{self.audio_track}.wav"

        result = model.transcribe(audio_file)
        if os.path.exists(audio_file):
            os.remove(audio_file)

        self.transcript_text = "transcribed_text"
        text_file_path = f"media/{self.transcribed_text}.txt"
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

    def generate_questions_gemini(self):
        input_filename = f"media/{self.transcribed_text}.txt"
        transcript = self.read_file(input_filename)

        prompt = f"""
            Create a quiz based on the following transcript.

            Requirements:
            - Generate exactly 10 multiple-choice questions.
            - Each question must have exactly 4 distinct answer options.
            - Each question must have exactly one correct answer.
            - Include the correct answer in the 'question_options'.
            - Do not include explanations, comments,
              or any text outside the JSON.
            - Answer in English only.
            - Return the output strictly in the following JSON format:

            {{
            "title": (
                "Create a concise quiz title based on the topic "
                "of the transcript."
            ),
            "description": (
                "Summarize the transcript in no more than 150 characters. "
                "Do not include any quiz questions or answers."
            ),
            "questions": [
                {
                    "question_title": "The question goes here.",
                    "question_options": [
                        "Option A",
                        "Option B",
                        "Option C",
                        "Option D"
                    ],
                    "answer": "The correct answer from the above options"
                }
            ]
            }}

            transcript:
            {transcript[:10000]}
            """

        response = CLIENT.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        self.generated_text = "generated_text"
        filename = f"media/{self.generated_text}.txt"
        self.write_file(filename, response.text)

    def edge_cleaner_text(self):
        filename = f"media/{self.generated_text}.txt"

        content = self.read_file(filename)
        content = content.strip()
        content = self.remove_markdown(content)
        self.write_file(filename, content)
        return content

    def remove_markdown(self, content):
        if content.startswith("```json"):
            content = content[len("```json "):]

        if content.endswith("```"):
            content = content[:-3]

        return content

    def read_file(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()

    def write_file(self, filename, content):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

    def delete_transcribed_text(self):
        if os.path.exists(f"media/{self.transcribed_text}.txt"):
            os.remove(f"media/{self.transcribed_text}.txt")

    def delete_generated_text(self):
        if os.path.exists(f"media/{self.generated_text}.txt"):
            os.remove(f"media/{self.generated_text}.txt")
