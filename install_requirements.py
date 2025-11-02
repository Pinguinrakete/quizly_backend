import subprocess
import sys
import os

def has_cuda():
    """Check if an NVIDIA GPU with CUDA support is available (without requiring torch)."""
    try:
        subprocess.run(
            ["nvidia-smi"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

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

def install_torch():
    """Install either the GPU or CPU version of PyTorch based on system capability."""
    if has_cuda():
        print("💪 CUDA-capable GPU detected → installing GPU version of PyTorch...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--upgrade",
            "torch", "torchvision", "torchaudio",
            "--index-url", "https://download.pytorch.org/whl/cu121"
        ])
    else:
        print("🧠 No NVIDIA GPU detected → installing CPU version of PyTorch...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--upgrade",
            "torch", "torchvision", "torchaudio",
            "--index-url", "https://download.pytorch.org/whl/cpu"
        ])

if __name__ == "__main__":
    print("🚀 Starting installation process...\n")
    upgrade_pip()
    install_requirements()
    install_torch()
    print("\n✅ All packages have been installed successfully!")
