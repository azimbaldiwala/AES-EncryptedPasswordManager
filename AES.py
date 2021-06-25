from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def get_hkey(key):
    """
    Used for making hkey form key.
    """
    hash_obj = SHA256.new(key.encode('utf-8'))
    hkey = hash_obj.digest()
    return hkey


def padding(msg):
    """
    padding msg so that it is divisible by 16.
    """
    BLOCK_SIZE = 16
    PAD = '*'
    return msg + (BLOCK_SIZE - len(msg) % BLOCK_SIZE ) * PAD


def encrypt(info, key):
    """
    As the name suggests, func() takes in info and key and encrypts the info using key with AES-ECB
    """
    cipher = AES.new(get_hkey(key), AES.MODE_ECB)
    result = cipher.encrypt(padding(info).encode('utf-8'))
    return result


def decrypt(info, key):
    """
    decrypts the encrypted info.
    """
    PAD = '*'
    decipher = AES.new(get_hkey(key), AES.MODE_ECB)
    pt = decipher.decrypt(info).decode('utf-8')
    pad_index = pt.find(PAD)
    result = pt[:pad_index]
    return result