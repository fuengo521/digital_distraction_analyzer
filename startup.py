import subprocess
import sys
import os
import platform

# Set up your Python environment
# Getting Started:
# In your Terminal
    # python -m venv venv
    # On Mac: source venv/bin/activate
    # On Windows: venv/Scripts/activate
    # python startup.py 
# Now you are good to go!

# Next time you start working:
    # On Mac: source venv/bin/activate
    # On Windows: venv/Scripts/activate

# Optional when you are done:
    # deactivate

def is_venv_active():
    """Returns True if running inside a virtual environment."""
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )

def print_activation_tip():
    os_name = platform.system()
    print("\n To activate your virtual environment, run:")

    if os_name == "Windows":
        print("  venv\\Scripts\\activate")
    else:  # macOS or Linux
        print("  source venv/bin/activate")

    print("\n Then re-run this script:\n  python startup.py")

def install_requirements():
    print("Installing packages from requirements.txt...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def create_directories():
    print("Creating folder structure...")
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("notebooks", exist_ok=True)
    os.makedirs("src", exist_ok=True)
    os.makedirs("visuals", exist_ok=True)
    os.makedirs("reports/figures", exist_ok=True)

def main():
    print("Initializing project setup...\n")
    
    if not is_venv_active():
        print("WARNING: You are not in an active virtual environment!")
        print_activation_tip()
        return
    
    install_requirements()
    create_directories()
    print("Project initialized!")

if __name__ == "__main__":
    main()
    sys.exit(0)