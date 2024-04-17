import os
import base64
import random
from Crypto.Cipher import AES


def encrypt_phrase(phrase: str) -> (bytes, bytes):
    """Function encrypts a phrase using AES key generated within the function.
    Inputs:
    phrase: The phrase to encrypt.
    Output:
    Encrypted phrase and the key used.
    """

    # Generate a 16-byte random key.
    key = os.urandom(16)

    # Create an AES cipher object with the generated key.
    cipher = AES.new(key, AES.MODE_CBC, iv=os.urandom(16))

    # Encode using the utf-8 character set and add the padding to the phrase.
    encoded_phrase = phrase.encode("utf-8")
    padded_phrase = pad(encoded_phrase, 16)

    # Encrypt the phrase.
    encrypted_phrase = cipher.encrypt(padded_phrase)

    # Encode the encrypted phrase to base64"
    encrypted_phrase = base64.b64encode(encrypted_phrase)

    # Return the output of encrypted phrase and the key.
    return encrypted_phrase, key


def pad(data: bytes, block_size: int) -> bytes:
    """ Function pads a string (Phrase entered by user) to a multiple of the specified block size to meet AES requirments.
    Inouts:
    data: The phrase to be pad.
    block_size: The block size to be pad to.
    Outpur:
    The padded string (Phrase).
    """

    # PKCS#7 padding is used to pad the data to the block size.
    padding_len = block_size - len(data) % block_size
    if padding_len == 0:
        padding_len = block_size

    padding = bytes([padding_len] * padding_len)
    return data + padding


if __name__ == "__main__":
    # Get the phrase to encrypt from the user.
    phrase = input("Enter the phrase to encrypt: ")

    # Encrypt the phrase.
    encrypted_phrase, key = encrypt_phrase(phrase)

    # Print the encrypted phrase, passphrase, and the key.
    print(f"Phrase: {phrase}")
    print(f"Key: {key}")
    print(f"Encryped Phrase: {encrypted_phrase}")
