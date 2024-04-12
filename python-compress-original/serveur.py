import os.path
import socket
import threading
import time
import  hauffman
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind(('0.0.0.0', 15554))
mySocket.listen()
numClient = 1


class traiter_client(threading.Thread):

    def __init__(self, conn, adress, numClient):

        super().__init__()

        self.con = conn
        self.adress = adress
        self.numClient = numClient

    def run(self):
        file_name = conn.recv(2048).decode("utf-8")
        print(f"Le serveur a reçu la demande pour le fichier : {file_name}")

        # Vérifier si le fichier existe
        if os.path.exists(file_name):
            fp = open(file_name, 'rb')
            encode_bytes = hauffman.compress_file(file_name).getvalue()
            file_size = os.path.getsize(file_name)
            pos = 0
            nbr_block = int(file_size / 4)
            print(f'Le nombre de blocs = {nbr_block}')

            print(f"taille {len(encode_bytes)}")

            conn.send(f"{len(encode_bytes)}|".encode())
            conn.send(encode_bytes)
            print(f'Le fichier {file_name} a été envoyé')
            time.sleep(10)
        else:
            print(f"Le fichier {file_name} n'existe pas.")

        conn.close()

try:
    while True:
        print("Attente des clients...")
        conn, adress = mySocket.accept()
        print(f'Un nouveau client numéro {numClient} est connecté')

        traiter_client(conn,adress,numClient).start() #il faut juste modifeir l'apel

        numClient += 1
except Exception as e:
    print(f'Il y a un problème : {e}')
finally:
    mySocket.close()