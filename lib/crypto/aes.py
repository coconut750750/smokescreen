import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

BACKEND = default_backend()
KEY_LENGTH = 32
IV_LENGTH = 16
BLOCK_LENGTH_BITS = 16 * 8

def get_cryptors(shared_key):
    assert len(shared_key) >= KEY_LENGTH + IV_LENGTH
    key = shared_key[:KEY_LENGTH]
    iv = shared_key[-IV_LENGTH:]
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=BACKEND)
    return cipher.encryptor(), cipher.decryptor()

if __name__ == '__main__':
    shared_key = os.urandom(KEY_LENGTH + IV_LENGTH)
    plaintext = b'a secret message not len 16'
    encryptor, decryptor = get_cryptors(shared_key)
    ciphertext1 = encryptor.update(plaintext)
    ciphertext2 = encryptor.update(plaintext)
    assert plaintext == decryptor.update(ciphertext1)
    assert plaintext == decryptor.update(ciphertext2)
