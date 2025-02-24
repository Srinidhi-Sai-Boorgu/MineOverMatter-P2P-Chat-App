import socket
import threading

class Peer:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.ip_addr = socket.gethostbyname(socket.gethostname())
        self.peers = {}  # { (ip, port): team name }
        self.mand_peers = [('10.206.4.122', 1255), ('10.206.5.228', 6555)]
        self.running = True
        self.lock = threading.Lock()
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind(('0.0.0.0', port))
        self.server_sock.listen(5)

    def decode_message(self, msg):
        ip = msg.split(':')[0]
        port = msg.split(':')[1].split(' ')[0]
        team_name = msg.split(':')[1].split(' ')[1]
        message = msg[msg.find(team_name[-1] + ' ')+2 ::]
        return ip, int(port), team_name, message

    def startServer(self):
        def clientHandle(client_sock, addr):
            while True:
                try:
                    data = client_sock.recv(1024).decode()
                    if not data:
                        break
                    _, sender_port, team_name, msg = self.decode_message(data)
                    if msg.strip().lower() == 'exit':
                        with self.lock:
                            if (addr[0], sender_port) in self.peers:
                                del self.peers[(addr[0], sender_port)]
                        print(f"\nPeer {addr[0]}:{sender_port} - {team_name} disconnected")
                        break
                    else:
                        with self.lock:
                            self.peers[(addr[0], sender_port)] = team_name
                        print(f"\n{addr[0]}:{sender_port} {team_name} {msg}")
                except Exception as e:
                    print(f"Error handling client: {e}")
                    break
            client_sock.close()
        while self.running:
            try:
                client_sock, addr = self.server_sock.accept()
                client_thread = threading.Thread(target=clientHandle, args=(client_sock, addr))
                client_thread.daemon = True
                client_thread.start()
            except:
                break

    def sendMsg(self, ip, port, msg):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                full_msg = f"{self.ip_addr}:{self.port}" + f" {self.name} " + msg
                s.send(full_msg.encode())
                print(f"Message sent to {ip}:{port}")
        except Exception as e:
            print(f"Failed to connect to {ip}:{port}: {e}")

    def peerConnect(self):
        for (ip, port), name in self.peers.items():
            self.sendMsg(ip, port, "Hello, this is a connection message")
            print(f"Connection established with {ip}:{port} - {name}")
            

    def peersQuery(self):
        if not self.peers:
            print("No connected peers")
        else:
            print("Connected Peers:")
            for i, ((ip, port), name) in enumerate(self.peers.items(), 1):
                print(f"{i}. {ip}:{port} - {name}")

    def cleanup(self):
        for (ip, port) in self.peers:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((ip, port))
                    full_msg = f"{self.ip_addr}:{self.port}" + f" {self.name} " + "exit"
                    s.send(full_msg.encode())
            except:
                continue
        self.running = False
        self.server_sock.close()

def main():
    name = input("Enter your name: ")
    port = int(input("Enter your port number: "))
    peer = Peer(name, port)
    server_thread = threading.Thread(target=peer.startServer)
    server_thread.daemon = True
    server_thread.start()
    print(f"Server listening on port {port}")
    for i, (ip, port) in enumerate(peer.mand_peers, 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                full_msg = f"{peer.ip_addr}:{peer.port}" + f" {peer.name} " + "This is a connection message"
                s.send(full_msg.encode())
                with peer.lock:
                    peer.peers[(ip, port)] = "MandatoryPeer" + str(i)
                print(f"Initialized connection with {ip}:{port}")
        except Exception as e:
            print(f"Failed to connect to {ip}:{port}: {e}")
    while True:
        print("\n***** Menu *****")
        print("1. Send message")
        print("2. Query active peers")
        print("3. Connect to active peers")
        print("0. Quit")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            ip = input("Enter the recipient's IP address: ").strip()
            port = int(input("Enter the recipient's port number: ").strip())
            msg = input("Enter your message: ").strip()
            peer.sendMsg(ip, port, msg)
        elif choice == '2':
            peer.peersQuery()
        elif choice == '3':
            peer.peerConnect()
        elif choice == '0':
            peer.cleanup()
            print("Exiting")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
