import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.fernet import Fernet
from base64 import b64decode
import socket


def get_payload(input_string):
    # Output : should be a dictionary as following
    # payload = {'key': contains encrypted key, 'data': contains encrypted data}

    # Split the input string into key and data
    # Since there is not "|" in the Base64 encoded data, we can use it as a separator
    key, data = input_string.split("|")

    return {'key': key, 'data': data}


def receive_data(private_key_path):
    # get the hostname
    host = socket.gethostname()
    # initiate port no above 1024
    port = 5000

    # get instance
    server_socket = socket.socket()
    # look closely. The bind() function takes tuple as argument. bind host address and port together
    server_socket.bind((host, port))

    # configure how many clients the server can listen simultaneously
    server_socket.listen(2)
    # accept new connection
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    while True:
        # receive data stream. it won't accept data packet greater than 4096 bytes
        data = conn.recv(4096).decode()
        if not data:
            # if data is not received break
            break
        payload = get_payload(str(data))
        # initiate hybrid decryption
        decr_ans = hybrid_dec(payload, private_key_path)
        print("Received message: " + str(decr_ans))

    conn.close()  # close the connection


def hybrid_dec(payload, private_key_path):
    # Read the private key
    with open(private_key_path, 'rb') as key_file:
        private_key = RSA.import_key(key_file.read())

    # Decode the symmetric key from base64
    enc_symmetric_key = b64decode(payload['key'])

    # Decode the data from base64
    enc_data = b64decode(payload['data'])

    # Decrypt the key with RSA and get the symmetric key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    symmetric_key = cipher_rsa.decrypt(enc_symmetric_key)

    # Decrypt the data
    fernet = Fernet(symmetric_key)
    data = fernet.decrypt(enc_data).decode("utf-8")

    return data


if __name__ == "__main__":
    # Get user input
    # Use .strip() function to remove any whitespaces from the begining and/or end of input value
    private_key_path = input("Enter the path to the Private key file (.pem): ").strip()

    # Check for the existence of both files
    if not os.path.isfile(private_key_path):
        print("Error: Private key file not found.")
    else:
        receive_data(private_key_path)
