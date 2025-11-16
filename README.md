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
    • JWT-Authentifizierung  |    Sicherer Login mit JSON Web Tokens
    • SQLite3                |    Database
    • yt-dlp                 |    Download the audio from the video.
    • Whisper                |    Transcribe the audio into text.
    • AI gemini-2.5-flash    |    Generate questions and answers from the text.

## ![Tech Stack Icon](assets/icons/folder.png) Project Structure
QUIZLY-BACKEND/  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── assets/  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;└── icons/  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── auth_app/  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;└── api/    
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── serializer.py  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── urls.py  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;└──  views.py  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;└── tests.py   
&emsp;&emsp;&nbsp;&emsp;&nbsp;│  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── core/  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;├── settings.py  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;└── urls.py  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── quiz_app/  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;└── api/    
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── permissions.py  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── serializer.py  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── urls.py  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── utils.py     
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;└──  views.py  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;├── admin.py  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;├── apps.py  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;├── models.py     
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;└── tests.py   
&emsp;&emsp;&nbsp;&emsp;&nbsp;│  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── env.template  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── db.sqlite3  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── manage.py  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── readme.md  
&emsp;&emsp;&nbsp;&emsp;&nbsp;└── requirements.txt  


















# ![Installation Icon](assets/icons/installation.png) Installation
## Windows 10/11
### 1. Python 3.11
Check if your Python version is 3.11, opening PowerShell or CMD and typing:
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
## LINUX
Check if your Python version is 3.11, opening bash and typing:
``` bash 
 python3 --version
 ``` 
Open bash:
``` bash 
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
```
 Check all installed Python Versions
``` bash 
ls /usr/bin/python* 
 ``` 
## MAC OS
Check if your Python version is 3.11, opening bash and typing:
``` bash 
 python3 --version
 ``` 
 ### 2. FFMPEG - Video encoder
Check if FFMPEG is installed by opening PowerShell or CMD and typing:
``` bash 
 FFMPEG -version
 ``` 
If winget is installed, open PowerShell or CMD and type:
``` bash 
winget install --id Gyan.FFmpeg -e --source winget
```
If winget is not installed: <br>
&nbsp;&nbsp;Download the latest FFmpeg build: https://ffmpeg.org/download.html <br>
&nbsp;&nbsp;Windows builds (usually from gyan.dev or BtbN).
<br><br>
Unpack the ZIP file, e.g., to C:\ffmpeg<br>
&nbsp;&nbsp;Go to the bin folder → ffmpeg.exe is located there. <br>
Add the bin path to the environment variables:<br>
&nbsp;•&nbsp;Right-click on 'This PC' → 'Properties' → 'Advanced system settings'.<br>
&nbsp;•&nbsp;Click 'Environment Variables...' → add the entry C:\ffmpeg\bin to the Path.

### 3. Clone the repository:
```bash
git clone https://https://github.com/Pinguinrakete/quizly_backend.git .
```   

### 4. Create a virtual environment to isolate our package dependencies locally
```bash
py -3.11 -m venv env   
``` 
### Windows
```bash
.\env\Scripts\activate
```  
### 5. Update pip
```bash
python -m pip install --upgrade pip
``` 
### 6. Install dependencies
```bash
pip install -r requirements.txt 
``` 
### 7. Migrations are applied to the database.
```bash
python manage.py migrate
```
### 8. Create a Admin User.
```bash
python manage.py createsuperuser
```
### 9. Generate a Gemini API-Key for model "gemini-2.5-flash"
```bash
1. Sign to your Google Cloud account.

2. Navigate to the API & Services → Credentials section.

3. Click Create Credentials → API Key.

4. Copy the generated key.

5. Use this key to authenticate requests to the gemini-2.5-flash model.
```
### 10. Creating and filling a .env
```bash
Please rename the .env.template to .env and set all necessary environment variables.

Generate a SCRET_KEY, please open the PowerShell:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
### 11. Start the server.
```bash
python manage.py runserver
```
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