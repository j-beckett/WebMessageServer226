#!/usr/bin/python3
import sys
import random 
import traceback
import string
import requests
import json


SERVER_HOST = sys.argv[1]
SERVER_PORT = sys.argv[2]
GET_URL = "http://" + SERVER_HOST + ':' + SERVER_PORT + '/' + "msgserver/get/"
POST_URL = "http://" + SERVER_HOST + ':' + SERVER_PORT + '/' + "msgserver/create/"
KEY_LENGTH = 8
MAX_MESSAGE_LENGTH = 160

MESSAGE_KEY_START = 10
MESSAGE_KEY_END = 18  

#takes no params, generates a random key for the next message in the linked list
# get random key of length KEY_LENGTH ( 8 ) with letters(upperCase & lowercase) + digits
def generateKey():
    characters = string.ascii_letters + string.digits
    randomKey = ''.join(random.choice(characters) for i in range(KEY_LENGTH))
    #print("Random password is:", randomKey)

    return randomKey

#this function prompts user for input. DOES ERROR CHECKING on usrInput and enforces the proper message length.
#Returns a VALID string to be saved into the message dictionary
def promptForMessage():
    print("Please enter a new message: \n")
    usrString = input()

    while len(usrString ) < 1 or len(usrString ) > MAX_MESSAGE_LENGTH:
        print("Invalid message size. Please input a message longer than 0 and less than " + str(MAX_MESSAGE_LENGTH) + "\n")
        usrString = input()

    return usrString

#takes no params
# calls upon generateKey to create a Key of KEY_LENGTH chars (8), then concats it with the usr provided string. 
# This message is then returned, and sent by createConnection.    
def generateMessageToServer(usrString):
    randomKey = generateKey()
    return(randomKey + usrString + "\n") #first KEY_LENGTH (8) bytes of message is the "nextKey"

#takes in the current messages's key (message_key) and the complete message to send to the server as params
#uses the requests library to add in the message and key as a "payload" to the url
def createConnection(message_key, messageToSend):
    client = requests.session()
    #url = POST_URL + message_key
    client.get(POST_URL)
    if 'csrftoken' in client.cookies:
        elements = {'message':messageToSend, 'key':message_key, 'csrfmiddlewaretoken':client.cookies['csrftoken']}
        post = client.post(POST_URL, data = elements, headers = {'Referer' : POST_URL})



#this function is the 'main' runner of the program. 
#takes in no params, however gets vars off the command line using sys.argv. 
#                                                                                    ###################check 4 invlaid input

#if there is no messages for a user provided key, starts a new message 'thread' (think reddit thread, not a multithreading thread)
#the message thread is implemented with a link list of keys. Each message containing the pointer to the next message in the first KEY_LENGTH (8) chars of the message
#if there is messages in the thread, continue printing messages until reaching an empty node (a "No message at key" message is found), then prompt usr for next message
#after new message is entered by user and sent, close the connection.
def client():
    try:
        message_key = sys.argv[3]
        if len(message_key) != KEY_LENGTH or message_key.isalnum() == False:
            print("Key length must be exactly " + str(KEY_LENGTH) + " chars and alphanumeric. Please try again.")
            sys.exit(-2)

        while(True): #Loop until a "No message at key" message is found. If found, break the loop and prompt user to enter a new message.
            response = requests.get(GET_URL + message_key + '/')
            data = response.text

            if (data == "No message at key"+ message_key):
                break

            print(data[MESSAGE_KEY_END - 1: ]) #the actual message starts after the key included in the message. this should account for changes in key length 
            message_key = (data[MESSAGE_KEY_START : MESSAGE_KEY_END])
            
            
        newUsrMessage = promptForMessage()
        createConnection(message_key, generateMessageToServer(newUsrMessage)) #generateMessageToServer joins random gen key with our user input. 

    except Exception as details:
                    print(details)
                    traceback.print_exc()
                    pass

    sys.exit(-1)

client()

