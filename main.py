import os
import json
import base64
import win32crypt
import sqlite3
from Crypto.Cipher import AES
import argparse

# Creating vars
ls_path = None
cookies_path = None
file_name = None

parser = argparse.ArgumentParser()

# Creating args
parser.add_argument("-ls", "--local-state", dest="ls_path", default=os.path.expandvars(r"%localappdata%\Google\Chrome\User Data\Local State"), help="Local State file location (Leave empty for default value)\n")
parser.add_argument("-cf", "--cookies-file", dest="cookies_path", default=os.path.expandvars(r"%localappdata%\Google\Chrome\User Data\Default\Cookies"), help="Cookies file location (Leave empty for default value)\n")
parser.add_argument("-o, --output", dest="file_name", default=f"{os.getcwd()}\cookies.json", help=f"Output file (default: \"{file_name}\")\n")

def parseArgs():
    global ls_path
    global cookies_path
    global file_name
    print(args.ls_path)
    print(args.cookies_path)
    print(args.file_name)
    ls_path = args.ls_path
    cookies_path = args.cookies_path
    file_name = args.file_name

def start():
    try:
        with open(ls_path, "r") as f:
            encrypted_key = json.load(f)['os_crypt']['encrypted_key']
    except FileNotFoundError:
        return print("Error: Invalid Local State file path")

    encrypted_key = base64.b64decode(encrypted_key)
    encrypted_key = encrypted_key[5:]
    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

    try:
        con = sqlite3.connect(cookies_path)
    except sqlite3.OperationalError:
        return print("Error: Invalid Cookies file path")
    cur = con.cursor()
    cookies: list = []
    for row in cur.execute("SELECT host_key, name, encrypted_value, expires_utc FROM cookies"):
        nonce = row[2][3:3+12]
        ciphertext = row[2][3+12:-16]
        tag = row[2][-16:]
        cipher = AES.new(decrypted_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        cookie = {
            "host": row[0],
            "name": row[1],
            "value": plaintext.decode("utf-8"),
            "expires_utc": row[3]
        }
        cookies.append(cookie)
    con.close()

    with open(file_name, "w") as file:
        json.dump(cookies, file, indent=4)

if __name__ == "__main__":
    args = parser.parse_args()
    parseArgs()
    start()