from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# ================================================================================================
# Functions
# ================================================================================================


def generate_key_pair():
    # First we generate the private key
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())

    # Then we can generate the public key
    public_key = private_key.public_key()

    return private_key, public_key


def derive_shared_key(receiver_private_key, sender_public_key):
    # Get the shared key based on receiver's private key and sender's public key
    shared_key = receiver_private_key.exchange(ec.ECDH(), sender_public_key)

    # Derive the shared key
    derived_key = hashes.Hash(hashes.SHA256(), default_backend())
    derived_key.update(shared_key)

    return derived_key.finalize()


def encrypt_message(plain_message, key):
    # Make the required IV of 16 bytes
    iv = os.urandom(16)

    # Make the cipher, encryptor, and tag
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plain_message) + encryptor.finalize()
    tag = encryptor.tag

    return iv, ciphertext, tag


def decrypt_message(ciphertext, key, iv, tag):
    # Set up the cipher and decryptor
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    plain_text = decryptor.update(ciphertext) + decryptor.finalize()
    return plain_text


# ================================================================================================
# Walkthrough
# ================================================================================================

# 1. Exchange public keys
user_A_keys = generate_key_pair()
user_B_keys = generate_key_pair()

# 2. On both ends, derive a key from the original key pair and the partners public key
shared_key_A = derive_shared_key(user_A_keys[0], user_A_keys[1])
shared_key_B = derive_shared_key(user_B_keys[0], user_B_keys[1])

# 3. One side generates a session key, encrypts it with derived key
session_key = os.urandom(32)
encrypted_session_key_A = encrypt_message(session_key, shared_key_A)

# 4. Partner decrypts the session key using derived key
decrypted_session_key_B = decrypt_message(encrypted_session_key_A[1], shared_key_B, encrypted_session_key_A[0], encrypted_session_key_A[2])

# 5. Use session key to encrypt+decrypt message
message = b"Jesse, look at me, you are a blowfish"  # Definitely not a breaking bad reference
encrypted_message = encrypt_message(message, session_key)
decrypted_message = decrypt_message(encrypted_message[1], session_key, encrypted_message[0], encrypted_message[2])

print("Original Message:", message)
print("Decrypted Message:", decrypted_message.decode())
