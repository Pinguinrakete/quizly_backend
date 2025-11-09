import subprocess
import sys
import os

def upgrade_pip():
    """Upgrade pip to the latest version."""
    print("⬆️ Upgrading pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

def install_requirements():
    """Install dependencies from requirements.txt."""
    requirements_file = "requirements.txt"
    if os.path.exists(requirements_file):
        print("📦 Installing dependencies from requirements.txt...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--upgrade",
            "--prefer-binary",
            "-r", requirements_file
        ])
    else:
        print(f"⚠️  File {requirements_file} not found, skipping dependency installation.")

if __name__ == "__main__":
    print("🚀 Starting installation process...\n")
    upgrade_pip()
    install_requirements()
    print("\n✅ All packages have been installed successfully!")