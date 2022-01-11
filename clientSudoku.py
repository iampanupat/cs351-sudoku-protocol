# Panupat   Chulaotrakul      NO.6210402488
# Chottanin Pitchayaaroonsith NO.6210406599

from socket import *

HOST = 'localhost'
PORT = 12020

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

        # Check Status Code
        if (readResponse(response.decode())):
            response = response.decode()
            response = response.split('/')
            board = eval(response[1].strip())
        else:
            response = response.decode()
            response = response.split('/')
            response = response[0].strip()
            print('\n' + response)
            exit()

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
            
            if (readResponse(answerResponse.decode())):
                response = answerResponse.decode()
                response = response.split('/')

                temp = response[0].split()
                temp = temp[0].strip()
                temp = int(temp)
                if (temp == 201):
                    response = response[1].strip()
                    response = eval(response)
                    board[response[0]][response[1]] = response[2]
                    blank_amount -= 1
                elif (temp == 202):
                    life_amount -= 1

            else:
                response = answerResponse.decode()
                response = response.split('/')
                response = response[0].strip()
                print('\n' + response + '\n')            

        if (life_amount == 0):
            print('\nYOU LOSE')
        elif (blank_amount == 0):
            print('\nYOU WIN')

        # Close TCP connection
        clientSocket.close()

    except ConnectionRefusedError as error:
        print("Socket Error: %s" % error)
    exit(0)

def readResponse(response):
    response = response.split()
    if (int(response[0]) > 400):
        return False
    return True

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