from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os


def decrypt_file(encrypted_file_path, private_key_path, output_file_path):
    # Use the proper read write formats where necessary (its missing in the code)
    # Read the encrypted data
    with open(encrypted_file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

    # Read the private key
    with open(private_key_path, "r") as key_file:
        private_key = RSA.import_key(key_file.read())

    # Decrypt the data with RSA
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher_rsa.decrypt(encrypted_data)

    # Write the decrypted data to the output file
    with open(output_file_path, "w") as decrypted_file:
        decrypted_file.write(decrypted_data.decode("utf-8"))

    print(f'Decryption complete. Decrypted file saved to: {output_file_path}')


if __name__ == "__main__":
    # Get user input
    # Use .strip() function to remove any whitespaces from the begining and/or end of input value
    encrypted_file_path = input("Enter the path to the encrypted file: ").strip()
    private_key_path = input("Enter the path to the private key file (.pem): ").strip()
    output_file_path = input("Enter the output path for the decrypted file: ").strip()

    # Check for the existence of both files
    if not (os.path.isfile(encrypted_file_path) and os.path.isfile(private_key_path)):
        print("Error: Encrypted file or private key file not found.")
    else:
        decrypt_file(encrypted_file_path, private_key_path, output_file_path)
