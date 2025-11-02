import torch, os, yt_dlp, whisper

class AudioQuestionGenerator:
    file = ''

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
            info = audio.extract_info(url, download=True) 
            self.file = "file"
            # self.filename = info['title']
            print(f"✅ Successfully downloaded", self.file)


    def transcribe_whisper(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🚀 Using device: {device}")
        model = whisper.load_model("small", device=device)  # "tiny = 75MB", "base = 142MB", "small = 466MB", "medium = 1,5GB", "large = 2,9GB"
        audio_file = f"media/{self.file}.wav"

        result = model.transcribe(audio_file)

        os.remove(audio_file)
        text_file_path = f"media/{self.file}.txt"
        with open(text_file_path, 'w', encoding='utf-8') as f:
            f.write(result['text'])

        print(f"✅ Transcription saved in {text_file_path}")