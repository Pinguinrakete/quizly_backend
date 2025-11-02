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