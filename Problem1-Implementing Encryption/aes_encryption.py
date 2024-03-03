import os
import base64
from cryptography.fernet import Fernet

def encrypt_phrase(phrase):
  
  # Generate a random key.
  key = 

  # Create a Fernet object with the key.
  

  # Encrypt the phrase, while enconding using the utf-8 character set. 
  encrypted_phrase = 

  # Return the encrypted phrase and key.
  return encrypted_phrase, key


if __name__ == "__main__":

  # Get the phrase to encrypt from the user.
  phrase = 

  # Encrypt the phrase, calling the encryption function.
  

  # Print the encrypted phrase and key