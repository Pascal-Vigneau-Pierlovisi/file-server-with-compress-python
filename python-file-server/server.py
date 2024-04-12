import os
import socket
import threading
import pickle
from io import BytesIO
import hauffman

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind(('0.0.0.0', 15555))
mySocket.listen()

class TraitementClient(threading.Thread):
    def __init__(self, conn, adress):
        super().__init__()
        self.conn = conn
        self.adress = adress

    def run(self):
        try:
            # Attente de la demande du client
            request = self.conn.recv(2048).decode("utf-8")

            if request == "get_files_list":
                # Envoi de la liste des fichiers dans le répertoire spécifié
                files_list = os.listdir('files')
                files_pickle = pickle.dumps(files_list)
                self.conn.sendall(files_pickle)

            else:
                file_path = f'files/{request}'  # Utilisation de request pour obtenir le nom du fichier
                
                if os.path.exists(file_path):
                    print(f"Le client {self.adress} demande le fichier {file_path}")

                    with open(file_path, 'rb') as fp:
                        content = fp.read()
                        compressed_data, data_size = hauffman.compress(content)
                        self.conn.send(data_size.to_bytes(4, byteorder='big'))
                        self.conn.send(compressed_data.getvalue())
                        print(f'Le fichier {file_path} a été envoyé.')
                else:
                    print(f"Le fichier {file_path} n'existe pas.")

        except Exception as e:
            print(f'Il y a un problème : {e}')
        finally:
            self.conn.close()

try:
    while True:
        print("Attente des clients...")
        conn, adress = mySocket.accept()
        print(f'Un nouveau client est connecté depuis {adress}')
        TraitementClient(conn, adress).start()
except Exception as e:
    print(f'Il y a un problème : {e}')
finally:
    mySocket.close()
