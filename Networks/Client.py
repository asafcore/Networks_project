import socket
import json
import time
import board
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 60000  # The port used by the server
FORMAT = 'utf-8'
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT
PLAYER = 'B'
SERVER = 'Y'
INPUT_REQUEST = "please input your move"
SERVER_MOVE = "server move is"
GAME_WON = 'GAME WON'
MATCH_WON = 'MATCH_WON'
GAME_START = 'GAME STARTED'
#


def start_client():
    client_socket.connect((HOST, PORT))  # Connecting to server's socket
    msg = client_socket.recv(1024).decode(FORMAT)  # "game is staring"
    print(msg)
    msg = client_socket.recv(1024).decode(FORMAT)  # "please input number of games"
    print(msg)
    Nog = input()
    client_socket.send(Nog.encode(FORMAT))         # sending number of games to the server
    while True:
        msg = client_socket.recv(1024).decode(FORMAT)  # receiving msg from server
        if msg == GAME_START:
            msg = client_socket.recv(1024).decode(FORMAT)
            print(msg)                                 # "game number {i} is staring"
            cur = board.Board()
        if msg == INPUT_REQUEST:
            print(msg)                                 # "please enter your move"
            cur.printBoard()                                 # "printing game board"
            move = input(msg)
            cur.insert(move, PLAYER)
            cur.printBoard()
            client_socket.send(move.encode(FORMAT))    # sending move to server
            print("sent to server")
        if msg == SERVER_MOVE:
            print(msg)
            move = client_socket.recv(1024).decode(FORMAT)
            print(move)
            cur.insert(move, SERVER)
            cur.printBoard()
        if msg == GAME_WON:
            msg = client_socket.recv(1024).decode(FORMAT)
            print(msg)                                 # "the winner of the game is ..."
        if msg == MATCH_WON:
            print(msg)
            break
    msg = client_socket.recv(1024).decode(FORMAT)
    print(msg)                                         # "the winner of the match is ..."
    msg = client_socket.recv(1024).decode(FORMAT)
    print(msg)                                         # "thanks for playing"
    client_socket.close()  # Closing client's connection with server (<=> closing socket)
    print("\n[CLOSING CONNECTION] client closed socket!")

if __name__ == "__main__":
    IP = socket.gethostbyname(socket.gethostname())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("[CLIENT] Started running")
    start_client()
    print("\nGoodbye client:)")