import socket
import pickle
import ssl

class FederatedClient:
    def __init__(self, client_id, host='127.0.0.1', port=5000):
        self.client_id = client_id
        self.host = host
        self.port = port

    def train_locally(self):
        local_weights = [float(self.client_id), 0.5 * self.client_id, 1.2 * self.client_id]
        return local_weights

    def run(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations(cafile="cert.pem")
        context.check_hostname = False 

        try:
            secure_client = context.wrap_socket(client_socket, server_hostname=self.host)
            secure_client.connect((self.host, self.port))
            print(f"[Client {self.client_id}] Secure TLS connection established with server.")

            weights = self.train_locally()
            payload = pickle.dumps(weights)
            secure_client.sendall(payload)

            response_data = secure_client.recv(4096)
            response = pickle.loads(response_data)
            print(f"[Client {self.client_id}] Server response: {response['message']}")

        except Exception as e:
            print(f"[Client {self.client_id}] Secure connection failed: {e}")
        finally:
            secure_client.close()