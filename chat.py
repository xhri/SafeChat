import asyncore
import inspect
from Connection import Connection
import sys
import colors
from encryptor import RSA

__author__ = 'rafal'

class Chat:
    CHAT_SYMBOL = ">"

    def __init__(self):
        self.connection = Connection(self.log)
        self.commands = []
        for i in inspect.getmembers(self, predicate=inspect.ismethod):
            if i[0] not in ['__init__', 'hello_message', 'main_loop', 'parse_command', 'wrong_command', 'log']:
                self.commands.append(i[0])

    def log(self, str, col=colors.BLACK):
        colors.printout(str + "\n", col)
        print(self.CHAT_SYMBOL, end="\r")

    def hello_message(self):
        print("Welcome to SafeChat v.0.99")
        print("Here should be some instructions, write help for more.")

    def parse_command(self, command):
        for com in self.commands:
            if com == command.split(' ')[0]:
                return getattr(self, com)(command)
        return True

    def main_loop(self):
        run = True
        while (run):
            print(self.CHAT_SYMBOL, end="\r")
            var = input()
            if len(var) == 0:
                continue
            if var[0] == ':':
                run = self.parse_command(var[1:])
            else:
                if self.connection.connected:
                    self.connection.send(var)
                else:
                    self.log("Sorry, you're not connected")

    def quit(self, com):
        asyncore.close_all()
        return False

    def listen(self, com):
        try:
            if len(str(com).split(' ')) != 2:
                raise Exception()
            port = int(str(com).split(' ')[1])
            self.log("Listening on port " + str(port))
            self.connection.listen(port)
        except OSError as e:
            self.log("Exception:")
            self.log(e.args[1])
        except Exception as e:
            self.log("Proper use of 'listen':")
            self.log(":listen %port_number%")
        return True

    def connect(self, com):
        try:
            if len(str(com).split(' ')) != 3:
                raise Exception()
            port = int(str(com).split(' ')[2])
            ip = str(com).split(' ')[1]
            self.log("Connecting to ip on port " + str(port))
            self.connection.connect(ip, port)
        except OSError as e:
            self.log("Exception:", colors.RED)
            self.log(e.args[1], colors.RED)
        except Exception as e:
            self.log("Proper use of 'connect'", colors.YELLOW)
            self.log(":connect %ip% %port%", colors.YELLOW)
        return True

    def disconnect(self, com):
        self.connection.stop_if_running()
        return True

    def help(self, com):
        self.log("Available commands:")
        for i in self.commands:
            self.log("-" + i)
        return True

    def h(self, com):
        return self.help(com)

    def set_key_len(self,com):
        try:
            if len(str(com).split(' ')) != 2:
                raise Exception()
            len = int(str(com).split(' ')[1])
            if not self.connection.connected:
                self.connection.crypto=RSA(self.log,len)
            else:
                self.log("You have to be disconnected",colors.YELLOW)
        except Exception as e:
            self.log("Proper use of 'set_key_len'", colors.YELLOW)
            self.log(":set_key_len %key_length_in_bits% ", colors.YELLOW)
        return True
