import socket


def StartClient(host, port):  # host is the server IP address
    ClientSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ClientSoc.connect(host, port)
    
    while True:
        msg = input('Enter a message: ')
        ClientSoc.send(msg.encode('utf-8')[:1024])

        response = ClientSoc.recv(1024).decode('utf-8')  # receive the message and decode it

        if response.lower() == 'Exit':
            break
        
        print(f'Received: {response}')

    ClientSoc.close()  # close the socket
    

################################
# Main 
################################

if __name__ == '__main__':
    ServerIP = '192.168.1.100'
    port = 2222
    
    StartClient(ServerIP, port)
    
    
        
    