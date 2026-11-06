import socket
import pickle
import threading
import ssl

class FederatedServer:
    def __init__(self, host='127.0.0.1', port=5000, total_clients=5):
        self.host = host
        self.port = port
        self.total_clients = total_clients
        self.active_connections = 0
        self.lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle_client(self, secure_conn, addr, client_id):
        print(f"[SERVER] Secure TLS Client {client_id} connected from {addr}")
        try:
            data = secure_conn.recv(4096)
            if data:
                weights = pickle.loads(data)
                print(f"[SERVER] Received encrypted weights from Client {client_id}: {weights}")
                
                response = pickle.dumps({
                    "status": "SUCCESS", 
                    "message": f"Encrypted weights from Client {client_id} securely received by server"
                })
                secure_conn.sendall(response)
        except Exception as e:
            print(f"[SERVER] Error handling Client {client_id}: {e}")
        finally:
            secure_conn.close()
            with self.lock:
                self.active_connections -= 1

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.total_clients)
        
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

        print(f"[SERVER] Secure TLS server is running on {self.host}:{self.port}, waiting for {self.total_clients} clients...")

        client_id = 1
        while client_id <= self.total_clients:
            conn, addr = self.server_socket.accept()
            
            try:
                secure_conn = context.wrap_socket(conn, server_side=True)
            except ssl.SSLError as e:
                print(f"[SERVER] SSL handshake failed with {addr}: {e}")
                conn.close()
                continue

            with self.lock:
                self.active_connections += 1
            
            thread = threading.Thread(target=self.handle_client, args=(secure_conn, addr, client_id))
            thread.start()
            client_id += 1

        print(f"[SERVER] All {self.total_clients} secure clients have finished communication.")
        self.server_socket.close()

if __name__ == "__main__":
    server = FederatedServer()
    server.start()