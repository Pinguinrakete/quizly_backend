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
## 1. Clone the repository:
```bash
git clone https://https://github.com/Pinguinrakete/quizly_backend.git .
```   
## 2. Create a virtual environment to isolate our package dependencies locally
```bash
python -m venv env
``` 
### Windows
```bash
.\env\Scripts\activate
```  

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