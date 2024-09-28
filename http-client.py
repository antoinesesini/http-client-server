import socket
import tkinter as tk
from tkinter import scrolledtext

# Fonction qui gère la connexion socket et affiche le résultat
def fetch_site_content():
    host = entry.get()  # Récupérer l'URL entrée
    path = "/"

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Créer une socket TCP
        ip_address = socket.gethostbyname(host) # Résoudre l'adresse IP à partir du nom d'hôte entré
        client_socket.connect((ip_address, 80)) # Connecter la socket au serveur (port 80 pour HTTP)

        # Préparer la requête HTTP GET
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        client_socket.sendall(request.encode())  # Envoyer la requête

        # Recevoir la réponse du serveur en morceaux de 4096 octets
        response = b""
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            response += data

        client_socket.close() # Fermer la connexion

        response_text = response.decode('utf-8', errors='replace') # Convertir la réponse en chaîne de caractères

        # Vérifier le code de statut HTTP : si pas correct on l'affiche en l'interprétant, sinon on affiche la réponse entière
        if "404 Not Found" in response_text:
            result_box.delete(1.0, tk.END)
            result_box.insert(tk.INSERT, "Erreur 404 : La page demandée n'existe pas.")
        elif "401 Unauthorized" in response_text:
            result_box.delete(1.0, tk.END)
            result_box.insert(tk.INSERT, "Erreur 401 : Non autorisé.")
        else:
            # Afficher la réponse complète
            result_box.delete(1.0, tk.END)
            result_box.insert(tk.INSERT, response_text)

    except Exception as e:
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.INSERT, f"Erreur lors de la requête : {e}")

# Création de la fenêtre principale
window = tk.Tk()
window.title("Client HTTP (Socket)")
# Label du champ d'entrée pour l'URL
label = tk.Label(window, text="Entrez l'URL (sans http://) :")
label.pack(pady=5)
# Champ d'entrée pour l'URL
entry = tk.Entry(window, width=50)
entry.pack(pady=5)
# Bouton pour lancer la requête
button = tk.Button(window, text="Envoyer la requête", command=fetch_site_content)
button.pack(pady=5)
# Ajout d'une zone de texte déroulante pour afficher le résultat
result_box = scrolledtext.ScrolledText(window, width=80, height=20)
result_box.pack(pady=10)
# Lancement de l'interface Tkinter
window.mainloop()
