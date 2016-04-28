# Tcp Chat server

import socket, select

#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        #if socket != server_socket and socket != sock :
        if socket != server_socket:
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)

if __name__ == "__main__":

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    INDEX_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 1024
    numberofclients = 0

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("192.168.0.12", PORT))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
    INDEX_LIST.append(numberofclients)
    print "Server started on port " + str(PORT)

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                sockfd.send('POLACZONO\n')
                if numberofclients < 3:
                    numberofclients = numberofclients + 1
                    login = sockfd.recv(1024)[6:]
                    print (login)
                    print ('number of clients: ', numberofclients)

                    CONNECTION_LIST.append(sockfd)
                    INDEX_LIST.append(numberofclients)
                    print "Player (%s, %s) connected" % addr

                    broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
                    if  numberofclients == 2: #start if more equal 10 players
                        broadcast_data(sockfd, 'START')

                else:
                    sockfd.send('ROOM IS FULL')

            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    if numberofclients < 3:
                        ind = 0 #to search id
                        for socket in CONNECTION_LIST:
                            ind = ind + 1
                            if socket != server_socket and socket == sock :
                                try :
                                    broadcast_data(sockfd, ind)
                                except :
                                    # broken socket connection may be, chat client pressed ctrl+c for example
                                    socket.close()
                                    CONNECTION_LIST.remove(socket)
                    else:
                        broadcast_data(sockfd, 'WAITING FOR PLAYERS')
                    #data = sock.recv(RECV_BUFFER)
                    #if data:
                    #    broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)

                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.close()
