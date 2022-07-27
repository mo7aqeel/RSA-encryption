#!/usr/bin/python                                              # This is server.py file
import pyDes
import socket  # Import socket module


s = socket.socket()  # Create a socket object
ip = '127.0.0.1'  # Get local machine name
port = 12320  # Reserve a port for your service.

s.bind((ip, port))  # Bind to the port

s.listen()  # Now wait for client connection.

connection, add = s.accept()  # Establish connection with client.

print('Got connection from', add)
connection.send('Thank you for connecting'.encode())

while True:
    # -----------------receive encrypted word list
    Encrypt_huge_listB = connection.recv(100000)
    # print("received Encrypted words as encoded bytes:", Encrypt_huge_listB, type(Encrypt_huge_listB))

    # Decode received data into UTF-8
    Encrypt_huge_listB = Encrypt_huge_listB.decode('utf-8')
    print("Decode received data into UTF-8:", Encrypt_huge_listB, type(Encrypt_huge_listB))

    # Convert decoded data into list
    Encrypt_huge_listB = eval(Encrypt_huge_listB)
    # print("Convert decoded data into list :", Encrypt_huge_listB, type(Encrypt_huge_listB))

    # ------------------------------------------------------------------------------------------

    # Decrypt
    Decrypted_wordsLst = []
    MasterKey = "DESCRYPT"
    k = pyDes.des(MasterKey, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    for i in range(0, len(Encrypt_huge_listB)):
        Decrypted_message = k.decrypt(Encrypt_huge_listB[i])
        Decrypted_wordsLst.append(str(Decrypted_message.decode()))

    print(Decrypted_wordsLst)
    print("________________________________ ")

    # ----------------------------Search section
    # receive word to  search for
    word = connection.recv(1024)
    # Decode received data into UTF-8
    word = word.decode('utf-8')
    print("this word you want to search : ", word, type(word))

    # search for word in the encrypted list
    msg = "The name is not found!"
    for i in range(len(Decrypted_wordsLst)):
        if word == Decrypted_wordsLst[i]:
            msg = Decrypted_wordsLst[i+2]

    print(msg)
    connection.send(msg.encode())

    # else:
    #         print("the word is not found :", word)
    #         msg = 'the word is not found'
    #         connection.send(msg.encode())
