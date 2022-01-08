from socket import *

HOST = 'localhost'
PORT = 12018

def main():
    try:
        # Try to connect to the server
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((HOST, PORT))

        print("\n================= The Sudoku Game =================")

        # Get difficulty from user until it's correct
        difficulty = input('Choose Your Difficulty ([E]asy-[N]ormal-[H]ard): ')
        while (checkDifficulty(difficulty) == 'error'):
            print("\nPlease type correctly, do it again")
            difficulty = input('Choose Your Difficulty ([E]asy-[N]ormal-[H]ard): ')

        board_number = int(checkDifficulty(difficulty))

        # Tell server how difficulty level that user choose
        request = "difficulty " + checkDifficulty(difficulty)
        clientSocket.send(request.encode())

        # Receive board number from server
        response = clientSocket.recv(1024)
        board = eval(response.decode())

        # Count all blank box
        blank_amount = 0
        for row in board:
            for col in row:
                if (int(col) == 0):
                    blank_amount += 1

        # Total Life
        life_amount = 0
        if (board_number == 0):
            life_amount = 5
        elif (board_number == 1):
            life_amount = 4
        elif (board_number == 2):
            life_amount = 3

        row_position = ''
        col_position = ''
        number = 0

        # Play Sudoku
        while (life_amount != 0 and blank_amount != 0):
            # Display the board
            print('\n====== Total Life x%d ======' % life_amount)
            printTable(board)
            row_position = input('- Select Row (A-I): ')
            col_position = input('- Select Column (1-9): ')
            number       = input('- Select Number (1-9): ')
            answerRequest = "answer " + str(board_number) + " " + row_position.upper() + " " + col_position + " " + number
            
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((HOST, PORT))            
            clientSocket.send(answerRequest.encode())
            answerResponse = clientSocket.recv(1024)

            payload = eval(answerResponse.decode())
            if (payload[0] == -1):
                life_amount -= 1
            else:
                board[payload[0]][payload[1]] = payload[2]
                blank_amount -= 1

        if (life_amount == 0):
            print('\nYOU NOOB!?!')
        elif (blank_amount == 0):
            print('\nYOU WIN <3')

        # Close TCP connection
        clientSocket.close()

    except ConnectionRefusedError as error:
        print("Socket Error: %s" % error)

    exit(0)

def checkDifficulty(difficulty):
    if (difficulty.lower() == 'e' or difficulty.lower() == 'easy'):
        return '0'
    elif (difficulty.lower() == 'n' or difficulty.lower() == 'normal'):
        return '1'
    elif (difficulty.lower() == 'h' or difficulty.lower() == 'hard'):
        return '2'
    else:
        return 'error'

def printTable(sudoku):
    print("    1 2 3   4 5 6   7 8 9  ")
    print("  +-------+-------+-------+")
    for row in range(9):
        print("%s | %s %s %s | %s %s %s | %s %s %s |" % (chr(row+65), 
            sudoku[row][0], sudoku[row][1], sudoku[row][2], 
            sudoku[row][3], sudoku[row][4], sudoku[row][5], 
            sudoku[row][6], sudoku[row][7], sudoku[row][8]))
        if ((row+1) % 3 == 0):
            print("  +-------+-------+-------+")

if __name__ == "__main__":
    main()