"""
Setup script to install Firestore dependencies and configure the environment.
"""

import subprocess
import sys
import os

def install_firestore_dependencies():
    """
    Install the required Google Cloud Firestore dependencies.
    """
    print("Installing Google Cloud Firestore dependencies...")
    
    try:
        # Install the required package
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "google-cloud-firestore"
        ])
        print("✅ Google Cloud Firestore library installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing Firestore dependencies: {e}")
        return False
    
    return True

def verify_installation():
    """
    Verify that the Firestore library is properly installed.
    """
    try:
        from google.cloud import firestore
        print("✅ Firestore library is properly installed and accessible")
        return True
    except ImportError as e:
        print(f"❌ Firestore library import failed: {e}")
        return False

def main():
    print("Firestore Integration Setup")
    print("=" * 30)
    
    # Install dependencies
    if install_firestore_dependencies():
        print("\nVerifying installation...")
        if verify_installation():
            print("\n🎉 Firestore integration is ready to use!")
            print("\nNext steps:")
            print("1. Configure your Firebase project settings")
            print("2. Set up authentication (service account key if needed)")
            print("3. Run your Django server")
            print("4. Access the new endpoints:")
            print("   - GET /alvos-sob-investigacao/firestore-users/")
            print("   - GET /monitorizacao-de-redes-sociais/nossa-comunidade/users/")
        else:
            print("\n❌ Installation completed but verification failed")
            print("Please check your Python environment and try again")
    else:
        print("\n❌ Installation failed. Please check your internet connection and try again.")

if __name__ == "__main__":
    main()