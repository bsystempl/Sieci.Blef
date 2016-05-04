# telnet program example
import socket, select, string, sys

def prompt() :
    #sys.stdout.write('<You> ')
    sys.stdout.flush()

def start():
    print sock.recv(4096)
    print sock.recv(4096)

def login():
    print s.recv(4096)
    msg = sys.stdin.readline()
    s.send(msg)
def game():
    print sock.recv(4096)
    msg = sys.stdin.readline()
    s.send(msg)

#main function
if __name__ == "__main__":



    host = "192.168.0.12"
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(40000)

    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host. Start sending messages'

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                login()
                if s.recv(4096)[:1] == "S":
                        start()
                else:
                        game()
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt()
            #user entered a message
            else :
                prompt()
