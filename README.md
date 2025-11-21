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
    • Python 3.11
    • Django 5.2.7
    • Django REST Framework 3.16.1
    • FFMPEG - Video encoder
    • JWT-Authentifizierung  |    Sicherer Login mit JSON Web Tokens
    • SQLite3                |    Database
    • yt-dlp                 |    Download the audio from the video.
    • Whisper                |    Transcribe the audio into text.
    • AI gemini-2.5-flash    |    Generate questions and answers from the text.

## ![Tech Stack Icon](assets/icons/folder.png) Project Structure
QUIZLY-BACKEND/  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── assets/  &emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&emsp;# Static project assets (images, files, etc.)  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;└── icons/ &emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Icon files used by the application   
&emsp;&emsp;&nbsp;&emsp;&nbsp;│  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── auth_app/  &nbsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Django app handling authentication features  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;└── api/    
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── serializers.py  &emsp;&emsp;&emsp;&nbsp;&emsp;# validates, converts, and represents data  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── urls.py &nbsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# API URL routes for authentication  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;└──  views.py  &nbsp;&nbsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# API URL routes for authentication  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;└── tests.py &emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Tests for authentication functionality   
&emsp;&emsp;&nbsp;&emsp;&nbsp;│  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── core/  &nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Main project configuration module  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;├── settings.py  &nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Django project settings (config, installed apps, etc.)  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;└── urls.py  &emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;# Root URL routing for the whole project  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── quiz_app/  &nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;# Django app handling quizzes and related features  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;└── api/    
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── permissions.py  &emsp;&emsp;&emsp;&nbsp;# Custom permissions for quiz API access  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── serializer.py   &nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;# Serializers for quiz-related models  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── urls.py  &nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;# API URL routes for quiz features  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── utils.py     &nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;&nbsp;# Helper functions: Download the audio, whisper, gemini  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;└──  views.py   &nbsp;&nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;# API endpoint logic for quizzes  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;├── admin.py   &nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;# Admin panel configuration for quiz models  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;├── apps.py  &nbsp;&nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Django app configuration  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;├── models.py     &nbsp;&nbsp;&nbsp;&nbsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Database models for quizzes  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;└── tests.py    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Tests for quiz functionality  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── env.template   &emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Template file for environment variables  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── db.sqlite3  &nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# SQLite database used for development  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── manage.py  &nbsp;&nbsp;&nbsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Django CLI management script  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── readme.md  &nbsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;# Project documentation and setup guide  
&emsp;&emsp;&nbsp;&emsp;&nbsp;└── requirements.txt  &emsp;&nbsp;&nbsp;&nbsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Python dependencies for the project  

# ![Installation Icon](assets/icons/installation.png) Installation
### 1. Install Python 3.11
Installed from https://www.python.org/downloads/<br>
### 2. FFMPEG - Video encoder
### Windows 10/11
&nbsp;&nbsp;Download the latest FFmpeg build: https://ffmpeg.org/download.html <br>
&nbsp;&nbsp;Windows builds (usually from gyan.dev or BtbN).
<br><br>
&nbsp;&nbsp;Unpack the ZIP file, e.g., to C:\ffmpeg<br>
&nbsp;&nbsp;Go to the bin folder → ffmpeg.exe is located there. <br>
&nbsp;&nbsp;Add the bin path to the environment variables:<br>
&nbsp;&nbsp;&nbsp;•&nbsp;Right-click on 'This PC' → 'Properties' → 'Advanced system settings'.<br>
&nbsp;&nbsp;&nbsp;•&nbsp;Click 'Environment Variables...' → add the entry C:\ffmpeg\bin to the Path.

### Linux
```bash
sudo apt update
sudo apt install ffmpeg 
```
### Mac OS
```bash
brew install ffmpeg 
```
### 3. Clone the repository:
```bash
create a folder "quizly_backend"
open the folder in VSCode
open the console
git clone https://github.com/Pinguinrakete/quizly_backend.git .
```   

### 4. Create a virtual environment to locally isolate our package dependencies and activate it.
### Windows 10/11
```bash
py -3.11 -m venv env   
.\env\Scripts\activate
``` 
### LINUX / MAC OS 
```bash
sudo apt install python3.11-venv
python3.11 -m venv env
source env/bin/activate
```  
### 5. Install dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt 
``` 
### 6. Generate a Gemini API-Key for model "gemini-2.5-flash"
```bash
1. Sign to your Google Cloud account.

2. Navigate to the API & Services → Credentials section.

3. Click Create Credentials → API Key.

4. Copy the generated key.

5. Use this key to authenticate requests to the gemini-2.5-flash model.
```
### 7. Please rename the .env.template to .env and set all necessary environment variables.
### Variables That Must Be Set:
&nbsp;&nbsp;&nbsp;•&nbsp;Insert the API key from step 6 into GEMINI_API_KEY=your_gemini_api_key  
&nbsp;&nbsp;&nbsp;•&nbsp;Next, generate a SECRET_KEY (see the lines below for Windows 10/11 or Linux/macOS)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;and replace SECRET_KEY_PLACEHOLDER with your generated value.
## 
### Windows 10/11
```bash
Generate a SCRET_KEY, please open the PowerShell:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
### LINUX / MAC OS 
```bash
Generate a SCRET_KEY, please open the bash:
python3 -c 'import secrets, string; chars="abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"; print("".join(secrets.choice(chars) for _ in range(50)))'
```
### 8. Migrations are applied to the database.
```bash
python manage.py makemigrations
python manage.py migrate
```
### 9. Create a Admin User.
```bash
python manage.py createsuperuser
```
### 10. Start the server.
```bash
python manage.py runserver
```
You can reach the backend at http://127.0.0.1:8000/
## ![API Endpoints Icon](assets/icons//api.png) API Endpoint Documentation
### ![Authentication Icon](assets/icons/authentication.png) Authentication 

| Method | Endpoint                 | Description                                       |
|--------|--------------------------|---------------------------------------------------|
| POST   | /api/auth/register/      | Registers a new user                              |
| POST   | /api/auth/login/         | Confirms identity and returns JWT tokens          |
| POST   | /api/auth/token/refresh/ | Refreshes expired authentication tokens for users |
| POST   | /api/auth/logout/        | Logs user out and clears session data             |

### ![Quiz Icon](assets/icons/quiz.png) Quiz Management
| Method | Endpoint          | Description                                     |
|--------|-------------------|-------------------------------------------------|
| POST   | /api/createQuiz/  | Creates a new quiz from a YouTube URL.          |
| GET    | /api/quizzes/     | Fetches all quizzes of the authenticated user   |
| GET    | /api/quizzes/{id} | Retrieves a specific quiz of the user           |
| PATCH  | /api/quizzes/{id} | Updates specific fields of a quiz.              |
| DELETE | /api/quizzes/{id} | Deletes a quiz along with all related questions |

### ![Quiz Icon](assets/icons/quiz.png) License
The license is under the MIT License.