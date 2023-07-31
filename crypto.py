# AES 256 encryption/decryption using pycryptodome library

from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
import os
from Cryptodome.Random import get_random_bytes
import json

password = "$8mS#pN2@zL7!kY$1rXw3Q9eA5gT"

cipher_text_key = 'RY8GJ0XPihgrRfUjciMY91bkKGX5znP8vY+QtApqYolfpKN1vvHJA8rVlgbokOBa8OJ'
salt_key = 'NUGCpefnsEOqLnuSHlWQQA/wlJMQCiP52TSZtNeJrCirYy/b9muUYe7fGpAeqIir+'
nonce_key = 'UxWSudGvEczw1ZIRDS/RP22WuKRg5nFsGkNeHfVsZ5EhB1h5mFa6r+t2zJ8jc'
tag_key = '79GYHXE96oQDKS3PHtDLi3iUvQ9lqNEpv1U1kD/nx9JBysev9rAsI/eTUQL/EscU2pERTJ0'
        
def encrypt(plain_bytes):
    # generate a random salt
    salt = get_random_bytes(AES.block_size)

    # use the Scrypt KDF to get a private key from the password
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return a dictionary with the encrypted text
    cipher_text, tag = cipher_config.encrypt_and_digest(plain_bytes)
    return {
        cipher_text_key: b64encode(cipher_text).decode('utf-8'),
        salt_key: b64encode(salt).decode('utf-8'),
        nonce_key: b64encode(cipher_config.nonce).decode('utf-8'),
        tag_key: b64encode(tag).decode('utf-8')
    }

def decrypt(enc_dict):
    # decode the dictionary entries from base64
    salt = b64decode(enc_dict[salt_key])
    cipher_text = b64decode(enc_dict[cipher_text_key])
    nonce = b64decode(enc_dict[nonce_key])
    tag = b64decode(enc_dict[tag_key])
    

    # generate the private key from the password and salt
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted


def main():
    # password = input("Password: ")

    # First let us encrypt secret message
    encrypted = encrypt("Hello im here")
    print(encrypted)

    # Let us decrypt using our original password
    decrypted = decrypt(encrypted)
    print(bytes.decode(decrypted))

# main()

