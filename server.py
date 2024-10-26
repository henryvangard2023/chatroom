import socket
import threading

################################
# Status:
# 
# Server is listening, waiting to implement the client 
#
# 10/8/24
################################

def StartServer(host, port):  # host should be the static IP address of the server which is 192.168.1.100

    serverSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSoc.bind((host,port))
    
    serverSoc.listen(5)
    print (f'Listening on port {port} ...')

    while True:
        clientSoc, clientIP = serverSoc.accept()
        print(f'Got a connection from {clientIP}')
        
        HandleClient(clientSoc)
        
def HandleClient(clientSoc):        
    try:
        while True:
            msg = clientSoc.recv(1024).decode('utf-8')
            if msg:
                print(f'Received: {msg}!')
                clientSoc.send(f'Echo: {msg}'.encode('utf-8'))
            else:
                break
    finally:
        clientSoc.close()

################################
# Main 
################################

ServerIP = 'localhost'
port = 2222

if __name__ == '__main__':
    StartServer(ServerIP, port)


