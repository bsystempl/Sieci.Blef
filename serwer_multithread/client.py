# telnet program example
import socket, select, string, sys

def prompt() :
    #sys.stdout.write('<You> ')
    sys.stdout.flush()

#main function
if __name__ == "__main__":

    host = "192.168.0.12"
    port = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print ('Unable to connect')
        sys.exit()

    print ('Connected to remote host. Start sending messages')
    prompt()

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print ('\nDisconnected from chat server')
                    sys.exit()
                else :
                    print data
                    sys.stdout.write(data)
                    msg = sys.stdin.readline()

            #user entered a message
            else :

                s.send(msg)
                prompt()
