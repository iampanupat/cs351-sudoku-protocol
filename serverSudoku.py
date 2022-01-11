# Panupat   Chulaotrakul      NO.6210402488
# Chottanin Pitchayaaroonsith NO.6210406599

from socket import *
import time

SERVER_PORT = 12020

def main():
    try:
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind(('', SERVER_PORT))
        serverSocket.listen(1)
        print('The server is ready to receive.\n')

        while True:
            connectionSocket, addr = serverSocket.accept()
            print(time.asctime(time.localtime(time.time())), '|', addr, 'connected')
            
            # show IP, PORT, REQUEST from client
            request = connectionSocket.recv(1024).decode()
            print(time.asctime(time.localtime(time.time())), '|', addr, request)

            readRequest(connectionSocket, addr, request)
            connectionSocket.close()
            print(time.asctime(time.localtime(time.time())), '|', addr, 'disconnected')

    except OSError as error:
        print("OSError: %s" % error)
    exit(0)

def readRequest(connectionSocket, addr, request):
    requestList = request.split()

    if (requestList[0] == 'difficulty'):
        if (len(requestList) == 2):
            status_code = '200 Success'
            response_msg = str(getBoard(int(requestList[1])))
        else:
            status_code = '401 ParametersNotCorrect'
            response_msg = ''

    elif (requestList[0] == 'answer'):
        if (len(requestList) == 5):
            answer = (checkAnswer(requestList))
            if (answer[0] != -1):
                status_code = '201 AnswerCorrect'
                response_msg = str(checkAnswer(requestList))
            else:
                status_code = '202 AnswerNotCorrect'
                response_msg = ''
        else:
            status_code = '401 ParametersNotCorrect'
            response_msg = ''            

    else:
        status_code = '404 CommandNotFound'
        response_msg = ''
        
    payload = status_code + ' / ' + response_msg
    connectionSocket.send(payload.encode())
    print(time.asctime(time.localtime(time.time())), '|', addr, payload)

def checkAnswer(parameterList):
    boardNO = int(parameterList[1])
    row     = ord(parameterList[2]) - 65
    col     = int(parameterList[3]) - 1
    number  = int(parameterList[4])
    answer  = [
        [
            ['6', '5', '2', '3', '9', '4', '8', '1', '7'],
            ['8', '4', '3', '7', '2', '1', '9', '5', '6'],
            ['1', '7', '9', '5', '8', '6', '2', '3', '4'],
            ['5', '2', '8', '1', '6', '3', '4', '7', '9'],
            ['9', '3', '6', '8', '4', '7', '5', '2', '1'],
            ['7', '1', '4', '9', '5', '2', '6', '8', '3'],
            ['3', '6', '5', '4', '1', '8', '7', '9', '2'],
            ['2', '8', '1', '6', '7', '9', '3', '4', '5'],
            ['4', '9', '7', '2', '3', '5', '1', '6', '8']
        ],
        [
            ['3', '6', '4', '9', '5', '2', '7', '1', '8'],
            ['7', '9', '8', '1', '6', '3', '4', '5', '2'],
            ['2', '5', '1', '7', '8', '4', '6', '9', '3'],
            ['5', '7', '9', '2', '4', '8', '3', '6', '1'],
            ['6', '8', '3', '5', '7', '1', '2', '4', '9'],
            ['4', '1', '2', '3', '9', '6', '5', '8', '7'],
            ['8', '2', '6', '4', '3', '9', '1', '7', '5'],
            ['1', '4', '5', '8', '2', '7', '9', '3', '6'],
            ['9', '3', '7', '6', '1', '5', '8', '2', '4']
        ],
        [
            ['8', '7', '2', '6', '4', '9', '5', '3', '1'],
            ['9', '1', '3', '2', '5', '8', '7', '6', '4'],
            ['5', '4', '6', '1', '7', '3', '2', '8', '9'],
            ['7', '9', '8', '3', '2', '5', '1', '4', '6'],
            ['1', '2', '5', '9', '6', '4', '3', '7', '8'],
            ['6', '3', '4', '8', '1', '7', '9', '5', '2'],
            ['2', '8', '1', '7', '3', '6', '4', '9', '5'],
            ['3', '5', '9', '4', '8', '2', '6', '1', '7'],
            ['4', '6', '7', '5', '9', '1', '8', '2', '3']
        ]
    ]
    if (int(answer[boardNO][row][col]) == number):
        return [row, col, number]
    else:
        return [-1]
    
def getBoard(level):
    question = [
        [
            ['6', '0', '2', '3', '0', '0', '8', '0', '7'],
            ['0', '0', '3', '0', '0', '1', '9', '5', '0'],
            ['1', '7', '9', '0', '0', '0', '0', '0', '4'],
            ['0', '0', '8', '0', '0', '0', '0', '7', '9'],
            ['0', '0', '0', '8', '0', '7', '0', '0', '0'],
            ['7', '1', '0', '0', '0', '0', '6', '0', '0'],
            ['3', '0', '0', '0', '0', '0', '7', '9', '2'],
            ['0', '8', '1', '6', '0', '0', '3', '0', '0'],
            ['4', '0', '7', '0', '0', '5', '1', '0', '8']
        ],
        [
            ['3', '0', '4', '9', '0', '2', '7', '0', '0'],
            ['0', '9', '0', '0', '0', '3', '0', '5', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '3'],
            ['5', '0', '0', '0', '4', '8', '3', '0', '1'],
            ['0', '0', '3', '0', '0', '1', '0', '0', '9'],
            ['0', '1', '2', '0', '0', '0', '0', '0', '0'],
            ['8', '0', '0', '4', '0', '0', '0', '7', '0'],
            ['0', '4', '5', '8', '0', '7', '0', '0', '0'],
            ['0', '0', '0', '6', '0', '0', '0', '2', '0']
        ],
        [
            ['0', '7', '0', '0', '4', '0', '0', '3', '1'],
            ['9', '1', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '7', '0', '2', '8', '0'],
            ['0', '0', '0', '0', '0', '5', '0', '0', '6'],
            ['1', '0', '5', '0', '0', '0', '3', '0', '0'],
            ['0', '0', '0', '8', '0', '0', '9', '0', '2'],
            ['0', '0', '1', '0', '3', '6', '0', '0', '0'],
            ['3', '0', '9', '0', '0', '0', '0', '0', '7'],
            ['4', '0', '0', '5', '0', '1', '0', '2', '0']
        ]
    ]
    return question[level]

if __name__ == "__main__":
    main()