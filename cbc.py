import json
from base64 import b64encode,b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad
from Cryptodome.Random import get_random_bytes


def cbc_encrypt(key,message):#Encrypts the json
    cipher = AES.new(int.to_bytes(key,16,'big'), AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    result = json.dumps({'iv':iv, 'ciphertext':ct})
    return result
def cbc_decrypt(key,message):#Decrypts the json
    try:
        b64 = json.loads(message)
        iv = b64decode(b64['iv'])
        ct = b64decode(b64['ciphertext'])
        cipher = AES.new(int.to_bytes(key,16,'big'), AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt
    except (ValueError, KeyError):
        print("Incorrect decryption")


