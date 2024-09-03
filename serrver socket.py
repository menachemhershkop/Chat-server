import socket
import select

server = socket.socket()
server.bind(("0.0.0.0", 2234))
server.listen()
inputs = [server]
client_names = {}
print("Chat started. Waiting for connection.")

userlist = {
    "avi": "pass123",
    "dani": "dani456",
    "mendi": "mendi789",
    "yosef": "yosef101"
}

def users(client):
    client.send("Welcome! Enter your username: ".encode())
    while True:
        username = client.recv(2048).decode()
        if username in userlist:
            client.send("Enter your password: ".encode())
            password = client.recv(2048).decode()
            if password == userlist[username]:
                inputs.append(client)
                client_names[client] = username
                client.send(f'Welcome {username}'.encode())
                break
            else:
                client.send("Wrong password.".encode())
        else:
            client.send("User not found.".encode())

while inputs:
    readables, _, _ = select.select(inputs, [], [])
    for i in readables:
        if i is server:
            client, port = server.accept()
            print(f'Connected to {port}')
            users(client)
        else:
            try:
                data = i.recv(2048).decode()
                if not data:
                    print(f'Client {client_names[i]} left')
                    inputs.remove(i)
                    del client_names[i]
                else:
                    message = f'{client_names[i]}: {data}'
                    for client in inputs:
                        if client != i and client != server:
                            try:
                                client.send(message.encode())
                            except Exception as e:
                                print(f'Failed to send message to client {client.getpeername()}: {e}')
                                inputs.remove(client)
                                del client_names[client]
                                print(f'Client {client.getpeername()} left')
            except Exception as e:
                print(e)
                inputs.remove(i)
                del client_names[i]
                print(f'Client {i.getpeername()} left')
server.close()
