import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.fernet import Fernet
from base64 import b64encode
import socket


def send_data(public_key_path):
    # since both code is running on same pc
    host = socket.gethostname()
    # socket server port number
    port = 5000

    # print host name
    print("\nThis is Host:", host)

    # instantiate
    client_socket = socket.socket()
    # connect to the server
    client_socket.connect((host, port))

    # get input
    message = input("Enter the message -> ")

    while message.lower().strip() != 'bye':
        # get payload / encrypted message
        payload = hybrid_enc(message, public_key_path)
        # send the payload
        client_socket.send(payload.encode())

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


def hybrid_enc(data, public_key_path):
    # Generate a random symmetric key
    # Generate a random key.
    symmetric_key = Fernet.generate_key()
    # Create a Fernet object with the key.
    fernet = Fernet(symmetric_key)

    # Read the public key
    with open(public_key_path, ) as key_file:
        public_key = RSA.import_key(key_file.read())

    # Encrypt data with symmetric key
    enc_data = fernet.encrypt(data.encode("utf-8"))

    # Convert to base64 for sending over the network
    b64_enc_data = b64encode(enc_data).decode('utf-8')

    # Encrypt the symmetric key with RSA
    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_symmetric_key = cipher_rsa.encrypt(symmetric_key)

    # Convert the symmetric key to base64 for sending
    b64_enc_symmetric_key = b64encode(enc_symmetric_key).decode('utf-8')

    out_msg = str(b64_enc_symmetric_key + "|" + b64_enc_data)

    print("\nPayload : ", out_msg)
    return out_msg


if __name__ == "__main__":
    # Get user input
    # Use .strip() function to remove any whitespaces from the begining and/or end of input value
    public_key_path = input("Enter the path to the Public key file (.pem): ").strip()

    # Check for the existence of both files
    if not os.path.isfile(public_key_path):
        print("Error: Public key file not found.")
    else:
        send_data(public_key_path)
