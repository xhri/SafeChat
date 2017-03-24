from safe_chat import SafeChatServer,SafeChatClient
from encryptor import RSA
import asyncore
from threading import Thread
__author__ = 'xhri'


class Connection:

    def __init__(self,log):
        self.server=None
        self.client=None
        self.thread=None
        self.log=log
        self.connected=False
        self.crypto = RSA(self.log)
        pass

    def loop(self):
        asyncore.loop(use_poll=True, timeout=1)
        self.connected=False
        self.log("Exited loop")

    def run_loop(self):
        if self.thread is None:
            self.thread = Thread(target=self.loop)
            self.thread.start()

    def stop_if_running(self):
        if self.server is not None:
            self.server.close()
        if self.client is not None:
            self.client.close()
        if self.thread is not None:
            self.thread.join()
            self.thread = None

    def listen(self, port):
        self.stop_if_running()
        self.server = SafeChatServer(self,self.crypto,'localhost',port)
        self.run_loop()

    def connect(self,ip,port):
        self.stop_if_running()
        self.client = SafeChatClient(self.log,self.crypto,ip,port)
        self.run_loop()
        self.connected=True

    def set_client(self, socket):
        self.client = socket
        self.connected=True

    def send(self,str):
        if self.client is not None:
            self.client.send(str)


