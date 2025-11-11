#  Quizly – Backend Description


![Features Icon](assets/icons/logoheader.png) 

This is the backend of Quizly, Quizly is an interactive quiz application that allows users to create, take, and manage quizzes. The application features a modern UI with a dark theme and green accents, providing an engaging user experience.
The core task of Quizly is to extract the audio track from a YouTube link, transcribe it using Whisper, and then use Gemini AI to generate ten questions, each with four possible answers, only one of which is correct.
The generated data is sent to the frontend as JSON.
For secure session management, a JWT authentication with HttpOnly cookies is used.

## ![Features Icon](assets/icons/gear.png) Features

- **User Authentication**: Register, login, logout and refresh token functionality
- **Quiz Generation**: Create quizzes from Youtube-URLs
- **Quiz Taking**: Interactive quiz interface with multiple-choice questions
- **Results Review**: View quiz results with correct/incorrect answers
- **Quiz Management**: View, edit, and delete quizzes  


## ![Tech Stack Icon](assets/icons/stack.png) Tech Stack
    • Python 3.11.9
    • Django 5.2.7
    • Django REST Framework 3.16.1
    • SQLite3            |    Database
    • yt-dlp             |    Download the audio from the video.
    • Whisper            |    Transcribe the audio into text.
    • KI Gemini Flash    |    Generate questions and answers from the text.
# ![Installation Icon](assets/icons/installation.png) Installation
# Windows 10/11
## 1. Python 3.11.9
Check if your Python version is 3.11.9, opening PowerShell or CMD and typing:
``` bash 
 py --version
 ``` 
If you have a different version, install version 3.11.9. <br> 
If winget is installed, open PowerShell or CMD and type:
``` bash 
winget install --id Python.Python.3.11 --version 3.11.9
``` 
If winget is not installed: <br>
Installed from https://www.python.org/downloads/<br><br>

Check all installed Python Versions
``` bash 
 py -0
 ``` 
 ## 2. FFMPEG - Video encoder
Check if FFMPEG is installed by opening PowerShell or CMD and typing:
``` bash 
 FFMPEG -version
 ``` 
If winget is installed, open PowerShell or CMD and type:
``` bash 
winget install --id Gyan.FFmpeg -e --source winget

```
If winget is not installed: <br>
Download the latest FFmpeg build: https://ffmpeg.org/download.html <br>
 Windows builds (usually from gyan.dev or BtbN).
<br><br>
Unpack the ZIP file, e.g., to C:\ffmpeg<br>
Go to the bin folder → ffmpeg.exe is located there. <br>Add the bin path to the environment variables:<br>
&nbsp;•&nbsp;Right-click on 'This PC' → 'Properties' → 'Advanced system settings'.<br>
&nbsp;•&nbsp;Click 'Environment Variables...' → add the entry C:\ffmpeg\bin to the Path.

## 3. Clone the repository:
```bash
git clone https://https://github.com/Pinguinrakete/quizly_backend.git .
```   

## 4. Create a virtual environment to isolate our package dependencies locally
```bash
py -3.11 -m venv env   
``` 
### Windows
```bash
.\env\Scripts\activate
```  
## 5. Update pip
```bash
python -m pip install --upgrade pip
``` 
## 6. Install dependencies
```bash
pip install -r requirements.txt 
``` 

<br><br><br>
### Authentication
POST &nbsp;&nbsp;&nbsp;/api/auth/register/<br>
POST &nbsp;&nbsp;&nbsp;/api/auth/login/<br>
POST &nbsp;&nbsp;&nbsp;/api/auth/token/refresh/<br>
POST &nbsp;&nbsp;&nbsp;/api/auth/logout/

### Quiz Management
POST &nbsp;&nbsp;&nbsp;/api/createQuiz/<br>
GET &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/api/quizzes/<br>
GET &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/api/quizzes/{id}<br>
PATCH &nbsp;&nbsp;/api/quizzes/{id}<br>
DELETE &nbsp;/api/quizzes/{id}