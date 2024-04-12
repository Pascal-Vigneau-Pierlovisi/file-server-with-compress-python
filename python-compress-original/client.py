import socket
from io import BytesIO

import hauffman

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.connect(('127.0.0.1', 15554))



# Demander le nom du fichier à télécharger
print("Entrez le nom du fichier à télécharger ")
file_name = input(">>")

try:
    mySocket.send(file_name.encode('utf-8'))
    print("envoie fait")

    # réception du contenu compressé

    # récupération de la taille
    size = ""

    while True:
        chr = mySocket.recv(1).decode()

        if chr == "|":
            break

        size += chr

    size = int(size)

    compressed_content = mySocket.recv(size)

    hauffman.decompress_file(BytesIO(compressed_content))

    mySocket.close()
except Exception as e:
    print(e)




# apres data dans la photo que j'ai prise  je mets a jour les elements suivant
#newMsg = True
#buf=msg[msgLen:]
#msg = ''
#break

#mySocket.close