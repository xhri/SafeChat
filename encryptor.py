
class NoEncryptor:
    def __init__(self,log):
        self.log=log
        self.log("Zrobiono NoEncryptor")
        pass

    def encrypt(self,data):
        return data.encode('UTF-8')

    def decrypt(self,data):
        return data.decode('UTF-8')