import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES

KEY = "uBy9ss3EK1"  # I just need credentials hidden from plain eye, not strictly protected


# copied from here https://stackoverflow.com/a/21928790/22052558
class AESCipher(object):
    def __init__(self):
        self.bs = AES.block_size
        self.key = hashlib.sha256(KEY.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw.encode())
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return AESCipher._unpad(cipher.decrypt(enc[AES.block_size:])).decode("utf-8")

    def _pad(self, s):
        return s + ((self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)).encode()

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
