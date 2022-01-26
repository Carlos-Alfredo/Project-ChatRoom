import json
from base64 import b64encode,b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad
from Cryptodome.Random import get_random_bytes
import time


def cbc_encrypt(key,message):#Encrypts the json
    tic=time.perf_counter()
    cipher = AES.new(int.to_bytes(key,16,'big'), AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    result = json.dumps({'iv':iv, 'ciphertext':ct}).encode()
    toc=time.perf_counter()
    with open('encrypted_timer.json') as f:
        encrypted_timer=json.load(f)
    encrypted_timer.append(toc-tic)
    with open('encrypted_timer.json', 'w') as f:
        json.dump(encrypted_timer,f)
    return result
def cbc_decrypt(key,message):#Decrypts the json
    tic=time.perf_counter()
    try:
        b64 = json.loads(message)
        iv = b64decode(b64['iv'])
        ct = b64decode(b64['ciphertext'])
        cipher = AES.new(int.to_bytes(key,16,'big'), AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        print(pt)
        toc=time.perf_counter()
        with open('decrypted_timer.json') as f:
            decrypted_timer=json.load(f)
        decrypted_timer.append(toc-tic)
        with open('decrypted_timer.json', 'w') as f:
            json.dump(decrypted_timer,f)
        return pt
    except (ValueError, KeyError):
        print("Incorrect decryption")


