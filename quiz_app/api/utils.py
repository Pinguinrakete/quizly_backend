import torch, os, yt_dlp, whisper
from google import genai
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

CLIENT = genai.Client(api_key=API_KEY)


class AudioQuestionGenerator:
    audio_track = 'audio_track'
    transcribed_text = 'transcribed_text'
    generated_text = 'generated_text'

    def download_audio(self, url):
        output_path = 'media'
        os.makedirs(output_path, exist_ok=True)

        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, 'audio_track'),
        'postprocessors': [{ 
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '0',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as audio:
            audio.extract_info(url, download=True) 
            self.audio_track = "audio_track"
            print(f"✅ Successfully downloaded", self.audio_track)


    def transcribe_whisper(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🚀 Using device: {device}")
        model = whisper.load_model("small", device=device) 
        audio_file = f"media/{self.audio_track}.wav"

        result = model.transcribe(audio_file)
        # os.remove(audio_file)
        
        self.transcript_text = result['text']
        filename = f"media/{self.transcribed_text}.txt"
        self.write_file(filename, self.transcribed_text)

        print(f"✅ Transcription saved in {filename}")


    def generate_questions_gemini(self):
        filename = f"media/{self.transcribed_text}.txt"
        transcript = self.read_file(filename)

        prompt = f"""
            Create a quiz based on the following transcript.

            Requirements:
            - Generate exactly 10 multiple-choice questions.
            - Each question must have exactly 4 distinct answer options.
            - Each question must have exactly one correct answer.
            - Include the correct answer in the 'question_options'.
            - Do not include explanations, comments, or any text outside the JSON.
            - Answer in English only.
            - Return the output strictly in the following JSON format:

            {{
            "title": "Create a concise quiz title based on the topic of the transcript.",
            "description": "Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.",
            "questions": [
                {{
                "question_title": "The question goes here.",
                "question_options": ["Option A", "Option B", "Option C", "Option D"],
                "answer": "The correct answer from the above options"
                }}
            ]
            }}

            transcript:
            {transcript[:10000]} 
            """

        response = CLIENT.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        self.generated_text = f"generated_text"
        filename = f"media/{self.generated_text}.txt"
        self.write_file(filename, response.text)
        # os.remove(transcribed_text)
        
        print(response.text)


    def edge_cleaner_text(self):
        filename = f"media/{self.generated_text}.txt"
        
        content = self.read_file(filename)
        content = content.strip()
        content = self.remove_markdown(content)
        self.write_file(filename, content) 


    def remove_markdown(self, content):      
        if content.startswith("```json"):
            content = content[len("```json "):]

        if content.endswith("```"):
            content = content[:-3]

        return content


    def read_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()


    def write_file(self, filename, content):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)