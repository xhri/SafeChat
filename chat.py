from safe_chat import SafeChatClient,SafeChatServer
import asyncore
from threading import Thread
from time import sleep
from encryptor import NoEncryptor
import inspect
from Connection import Connection
import curses

__author__ = 'rafal'

class Chat:

    def __init__(self):
        self.connection = Connection(self.log)
        self.commands = []
        for i in inspect.getmembers(self, predicate=inspect.ismethod):
            if i[0] not in ['__init__', 'hello_message', 'main_loop', 'parse_command','wrong_command','log']:
                self.commands.append(i[0])

    def log(self,str):
        print(str)

    def hello_message(self):
        print("Welcome to SafeChat v.0.1")
        print("Here will be some instructions")

    def parse_command(self,command):
        for com in self.commands:
            if com in command:
                return getattr(self, com)(command)
        return True

    def wrong_command(self):
        self.log("Wrong command.")

    def main_loop(self):
        run=True
        while(run):
            var = input()
            if var[0]== ':':
                run=self.parse_command(var[1:])
            else:
                if self.connection.connected:
                    self.connection.send(var)

    def quit(self, com):
        asyncore.close_all()
        return False

    def listen(self,com):
        if len(str(com).split(' ')) != 2:
            self.wrong_command()
        try:
            port = int(str(com).split(' ')[1])
            self.log("Listening on port "+str(port))
            self.connection.listen(port)
        except Exception as e:
            self.wrong_command()
        return True

    def connect(self,com):
        if len(str(com).split(' ')) != 2:
            self.wrong_command()
        try:
            port = int(str(com).split(' ')[1])
            self.log("Connecting to ip on port "+str(port))
            self.connection.connect('localhost', port)
        except Exception as e:
            self.wrong_command()
        return True


def main():

    chat=Chat()
    chat.hello_message()
    chat.main_loop()

if __name__=="__main__":
    main()