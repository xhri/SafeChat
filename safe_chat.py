import asyncore, socket
import pickle
import colors
__author__ = 'xhri'


class SafeChatServer(asyncore.dispatcher):
    def __init__(self, connection,crypto, host, port):
        asyncore.dispatcher.__init__(self)
        self.connection=connection
        self.crypto=crypto
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            self.connection.set_client(SafeChatClient(self.connection.log,self.crypto, sock))
            self.close()


class SafeChatClient(asyncore.dispatcher):

    def __init__(self,log,crypto,ip,port=-1):
        if port == -1:
            asyncore.dispatcher.__init__(self,ip)
        else:
            asyncore.dispatcher.__init__(self)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect((ip,port))
        self.log=log
        self.got=False
        self.crypto=crypto
        self.buffer=''
        asyncore.dispatcher.send(self,pickle.dumps(self.crypto.public))

    def writable(self):
        return ( len(self.buffer) > 0 )

    def handle_write(self):
        self.send(self.buffer)
        self.buffer=''

    def handle_read(self):
        data = self.recv(8192)
        if not self.got:
            self.crypto.enc=pickle.loads(data)
            self.got=True
        else:
            self.log(self.crypto.decrypt(data), colors.GREEN)

    def handle_error(self):
        self.log("Cant connect to given socket")

    def handle_close(self):
        self.close()

    def send(self, data):
        asyncore.dispatcher.send(self, self.crypto.encrypt(data)[0])




