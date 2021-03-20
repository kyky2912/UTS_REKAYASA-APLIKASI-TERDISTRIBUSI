#imports
import socket
import select

HEADER= 1

IP = "127.0.0.1"
PORT = 8888

#Membuat socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Alamat socket digunakan kembali
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()

#List socket/(socket.socket())
sockets_list = [server_socket]

#List client
clients = {}
print(f'Mendapatkan koneksi baru dari {IP}:{PORT}...')

#Pesan Masuk
def receive_message(client_socket):

    try:
        message_header = client_socket.recv(HEADER)

        #data tidak ditemukan
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False

while True:
    # Notifikasi Input/Output
    read_sockets, _ , exception_sockets = select.select(sockets_list, [], sockets_list)

    for socket_notifikasi in read_sockets:
        if socket_notifikasi == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user

            print('Koneksi baru diterima dari {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

        else:

            message = receive_message(socket_notifikasi)
            if message is False:
                print('Koneksi telah ditutup oleh: {}'.format(clients[socket_notifikasi]['data'].decode('utf-8')))
                sockets_list.remove(socket_notifikasi)
                del clients[socket_notifikasi]

                continue

            user = clients[socket_notifikasi]

            print(f'Pesan diterima dari: {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            for client_socket in clients:
                if client_socket != socket_notifikasi:

                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    #Handling socket exception
    for socket_notifikasi in exception_sockets:
        sockets_list.remove(socket_notifikasi)
        del clients[socket_notifikasi]
