import Crypto
from Crypto.PublicKey import RSA as RSAL
from Crypto import Random
import colors


class NoEncryptor:
    def __init__(self,log):
        self.log=log
        self.public=0
        self.enc=0
        self.log("Zrobiono NoEncryptor")
        pass

    def encrypt(self,data):
        return data.encode('UTF-8')

    def decrypt(self,data):
        return data.decode('UTF-8')


class RSA:
    def __init__(self,log,len=1024):
        self.log=log
        self.log("Generating RSA key...")
        self.key=RSAL.generate(len)
        self.log("RSA key generated",colors.GREEN)
        self.public=self.key.publickey()
        self.enc=None


    def encrypt(self,data):
        if self.enc is not None:
            return self.enc.encrypt(data.encode('UTF-8'),32)
        else:
            return 0

    def decrypt(self,data):
        return self.key.decrypt((data,)).decode('UTF-8')