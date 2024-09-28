import socket
import os


def handle_request(client_socket):

    request = client_socket.recv(1024).decode() # Recevoir la requête du client

    request_lines = request.splitlines() # Extraire le chemin de la requête
    if len(request_lines) > 0:
        # Extraire la méthode et le chemin de la requête
        request_line = request_lines[0]
        method, path, _ = request_line.split()

        if method == "GET": # Traiter uniquement les requêtes GET
            if path == "/": # Si pas de chemin on redirige vers /index.html
                path = "/index.html"  # Redirige vers index.html
            file_path = "." + path  # Ajoute le répertoire courant

            if os.path.isfile(file_path): # Vérifier si le fichier existe
                with open(file_path, 'rb') as f:
                    content = f.read()
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
                client_socket.sendall(response.encode() + content)
            else: # Fichier non trouvé
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
                response += "<html><body><h1>404 Not Found</h1><p>Le fichier demandé n'existe pas.</p></body></html>"
                client_socket.sendall(response.encode())
        else: # Méthode non supportée
            response = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\n\r\n"
            response += "<html><body><h1>405 Method Not Allowed</h1></body></html>"
            client_socket.sendall(response.encode())
    client_socket.close()


def run_server(port=80):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Créer une socket TCP
    server_socket.bind(("", port))
    server_socket.listen(5)
    print(f"Serveur HTTP en écoute sur le port {port}...")

    while True:
        # Accepter une connexion entrante
        client_socket, addr = server_socket.accept()
        print(f"Connexion acceptée de {addr}")
        handle_request(client_socket)


if __name__ == "__main__":
    run_server()
