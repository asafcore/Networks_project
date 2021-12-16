# Imports
# import sys
import socket
# import threading
import threading
# import board
import board
# import time
import time
# import random
import random
# import json
import json

# Define constants
HOST = '127.0.0.1'  # Standard loopback IP address (localhost)
PORT = 60000  # Port to listen on (non-privileged ports are > 1023)
FORMAT = 'utf-8'  # Define the encoding format of messages from client-server
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT
PLAYER = 'B'
SERVER = 'Y'
PLAYER_WIN_MSG = 'player has won the game'
SERVER_WIN_MSG = 'server has won the game'
GAME_WON = 'GAME WON'
MATCH_WON = 'MATCH_WON'
GAME_START = 'GAME STARTED'
#
# Function that handles a single client connection
# Operates like an echo-server
def handle_client1(conn, addr):
    print('[CLIENT CONNECTED] on address: ', addr)  # Printing connection address
    total_messages = conn.recv(1024).decode(FORMAT)  # Receiving from client # of messages to expect
    received = 0

    try:
        for i in range(int(total_messages)):
            data = conn.recv(1024).decode(FORMAT)
            print(f"Recieved message #{received} from client: \"" + data + "\"")
            conn.send(data.encode(FORMAT))
            received += 1
        print("\n[CLIENT DISCONNECTED] on address: ", addr)
        print()
    except:
        print("[CLIENT CONNECTION INTERRUPTED] on address: ", addr)


# Function that handles the second parallel client
# Only when 2 clients are connected simultaneously, this function will handle the second client
def handle_client2(conn, addr):
    print('[CLIENT CONNECTED] on address: ', addr)  # Printing connection address
    received = 0

    try:
        conn.send("Welcome! This is your server:)\nPlease enter your name:".encode(FORMAT))
        name = conn.recv(1024).decode(FORMAT)
        print("Received name from client: \"" + name + "\"")

        conn.send(f"Hello {name}!\nWhat is your age?".encode(FORMAT))
        age = conn.recv(1024).decode(FORMAT)
        print("Received age from client: \"" + age + "\"")

        conn.send("What is your profession?".encode(FORMAT))
        profession = conn.recv(1024).decode(FORMAT)
        print("Received profession from client: \"" + profession + "\"")

        time.sleep(0.01)
        conn.send("Nice to meet you:)\nGoodbye for now...".encode(FORMAT))
        print("[CLIENT DISCONNECTED] on address: ", addr)
        print()
    except:
        print("[CLIENT CONNECTION INTERRUPTED] on address: ", addr)


# function that handles a game with a client
def handle_game(conn, addr):
    print("the game is starting...")

    try:
        conn.send("the game is starting...".encode(FORMAT))
        conn.send("please enter the number of games you necessary to win".encode(FORMAT))
        Nog = conn.recv(1024).decode(FORMAT)
        Nog = int(Nog)
        games_won_server = 0
        games_won_player = 0
        counter = 0
        while (games_won_server != Nog) & (games_won_player != Nog):      # the game process for the entire set of games
            print(f"game number {counter} is starting")
            conn.send(GAME_START.encode(FORMAT))
            conn.send(f"game number {counter} is starting".encode(FORMAT))  # notifies which game is starting
            cur = board.Board()                                       # creates the board object
            while True:
                cur.printBoard()                                      # prints the board to the server
                print("\nwaiting for response from player")
                conn.send("please input your move".encode(FORMAT))
                move = conn.recv(1024).decode(FORMAT)                 # receives the column from the player
                cur.insert(move, PLAYER)                              # inserts the move of the player
                cur.printBoard()
                if cur.checkForWin() == PLAYER:                                 # checks for win
                    games_won_player = games_won_player + 1           # counts win for player
                    break

                move = random.randrange(1, 7, 1)                    # randomly chooses column
                move = str(move)
                conn.send("server move is".encode(FORMAT))            # notifies the player of server move
                conn.send(move.encode(FORMAT))                        # sends the move to the player
                cur.insert(move, SERVER)                              # inserts the server move
                if cur.checkForWin() == SERVER:                                 # checks for win
                    games_won_server = games_won_server + 1           # counts win for server
                    break
            msg = cur.checkForWin()
            conn.send(GAME_WON.encode(FORMAT))
            conn.send(f"the winner of game {counter} is{msg}".encode(FORMAT))           # notifies who won the game
            counter = counter + 1
        print(counter)
        conn.send(MATCH_WON.encode(FORMAT))
        conn.send(f"the winner of the match is {msg}".encode(FORMAT))
        conn.send("thanks for playing ...".encode(FORMAT))
        print("[CLIENT DISCONNECTED] on address: ", addr)
    except:
        print("[CLIENT CONNECTION INTERRUPTED] on address: ", addr)


# Function that starts the server
def start_server():
    server_socket.bind(ADDR)  # binding socket with specified IP+PORT tuple

    print(f"[LISTENING] server is listening on {HOST}")
    server_socket.listen()  # Server is open for connections

    while True:
        if threading.activeCount() == 1:  # Checking if no clients connected to the server client in total
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}\n")  # printing the amount of threads working

        connection, address = server_socket.accept()  # Waiting for client to connect to server (blocking call)

        if threading.activeCount() <= 5:
            thread = threading.Thread(target=handle_game, args=(connection, address))  # Creating new Thread object.
            # Passing the handle func and full address to thread constructor
            thread.start()  # Starting the new thread (<=> handling new client)
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}\n")  # printing the amount of threads working
        # on this process (opening another thread for next client to come!)


# Main
if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())  # finding your current IP address

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Opening Server socket

    print("[STARTING] server is starting...")
    start_server()

    print("THE END!")
