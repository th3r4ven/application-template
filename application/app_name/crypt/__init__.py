from Crypto.Cipher import AES
from os import environ

import base64
import unidecode

import logging
log = logging.getLogger("app_name." + __name__)


def encrypt(data):
    try:
        key = environ['CRYPT_KEY']
        symmetric = False
        clean_text = unidecode.unidecode(data)
        log.debug(f"Encrypt: clean_text: {clean_text}")
        cont = len(clean_text)
        while not symmetric:
            if (cont % 16) == 0:
                symmetric = True
            else:
                cont += 1

        aes = AES.new(key.encode(), AES.MODE_ECB)
        crypted_text = aes.encrypt(clean_text.rjust(cont).encode())
        crypted_text = base64.b64encode(crypted_text)
        log.debug(f"Encrypt: crypted_text {crypted_text.decode()}")
        return crypted_text.decode()
    except AttributeError as e:
        log.debug(f"Error encrypting data. Error: {e}")
        return data


def decrypt(data):
    try:
        key = environ['CRYPT_KEY']
        aes = AES.new(key.encode(), AES.MODE_ECB)
        crypted_text = data.encode()
        log.debug(f"Decrypt: data {data}")
        crypted_text = base64.b64decode(crypted_text)
        clean_text = aes.decrypt(crypted_text)
        clean_text = clean_text.decode('utf-8')
        log.debug(f"Decrypt: clean_text {clean_text.lstrip()}")
        return clean_text.lstrip()
    except Exception as e:
        log.debug(f"Error decoding model data. Error: {e}")
        return data
