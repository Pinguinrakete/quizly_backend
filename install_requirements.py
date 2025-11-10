import subprocess
import os

def run_command(command, shell=True):
    """Hilfsfunktion zum Ausführen von Shell-Befehlen."""
    print(f"💻 Running: {command}")
    subprocess.check_call(command, shell=shell)

def create_venv():
    """Erstellt ein virtuelles Python-Environment."""
    if not os.path.exists("env"):
        print("🌱 Creating virtual environment...")
        run_command("py -3.11 -m venv env")
    else:
        print("✅ Virtual environment already exists.")

def upgrade_pip():
    """Upgrade pip innerhalb des virtuellen Environments."""
    print("⬆️ Upgrading pip...")
    run_command(r".\env\Scripts\python.exe -m pip install --upgrade pip")

def install_requirements():
    """Install dependencies from requirements.txt inside the virtual environment."""
    requirements_file = "requirements.txt"
    if os.path.exists(requirements_file):
        print("📦 Installing dependencies from requirements.txt...")
        run_command(rf".\env\Scripts\python.exe -m pip install --upgrade --prefer-binary -r {requirements_file}")
    else:
        print(f"⚠️  File {requirements_file} not found, skipping dependency installation.")

def django_migrations():
    """Führt Django-Migrationen aus."""
    print("🛠️  Running Django migrations...")
    run_command(r".\env\Scripts\python.exe manage.py makemigrations")
    run_command(r".\env\Scripts\python.exe manage.py migrate")

if __name__ == "__main__":
    print("🚀 Starting full setup process...\n")
    create_venv()
    upgrade_pip()
    install_requirements()
    django_migrations()
    print("\n✅ Setup completed successfully!")