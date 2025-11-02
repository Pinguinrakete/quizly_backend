import torch, os, yt_dlp, whisper
from google import genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

CLIENT = genai.Client(api_key=API_KEY)


class AudioQuestionGenerator:
    file = 'file'

    def download_audio(self, url):
        output_path = 'media'
        os.makedirs(output_path, exist_ok=True)

        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, 'file'),
        'postprocessors': [{ 
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '0',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as audio:
            audio.extract_info(url, download=True) 
            self.file = "file"
            print(f"✅ Successfully downloaded", self.file)

    def transcribe_whisper(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🚀 Using device: {device}")
        model = whisper.load_model("small", device=device) 
        audio_file = f"media/{self.file}.wav"

        result = model.transcribe(audio_file)
        
        self.transcript_text = f"text_transcript"
        text_file_path = f"media/{self.transcript_text}.txt"
        os.remove(audio_file)
        with open(text_file_path, 'w', encoding='utf-8') as f:
            f.write(result['text'])

        print(f"✅ Transcription saved in {text_file_path}")

    def generate_questions_gemini(self):
        prompt = "Wie macht die Katze? Antworte in einem Satz"

        response = CLIENT.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        self.generated_text = f"generated_text"
        file_path = f"media/{self.generated_text}.txt"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(response.text)