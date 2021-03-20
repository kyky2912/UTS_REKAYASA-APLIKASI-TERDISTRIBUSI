#imports
import sys
import socket
import select
import errno

HEADER= 1

IP = "127.0.0.1"
PORT = 8888
my_username = input("Masukkan Username Anda: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

#Membangun koneksi untuk tidak memblok .recv()
client_socket.setblocking(False)
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER}}".encode('utf-8')
client_socket.send(username_header + username)

while True:

    #User Input Usernamenya
    message = input(f'{my_username} > ')
    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        while True:

            username_header = client_socket.recv(HEADER)

            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            panjang_username= int(username_header.decode('utf-8').strip())
            username = client_socket.recv(panjang_username).decode('utf-8')
            message_header = client_socket.recv(HEADER)
            panjang_message = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(panjang_message).decode('utf-8')

            print(f'{username} > {message}')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Terjadi error: {}'.format(str(e)))
            sys.exit()

        continue

    except Exception as e:
        #Exit ketika terjadi error
        print('Terjadi error: {}'.format(str(e)))
        sys.exit()
