import base64

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def get_aes_key(key: str) -> bytes:
    # Ensure key is 16, 24, or 32 bytes long by padding or truncating the string
    return key.encode('utf-8').ljust(32, b'\0')[:32]


def encrypt_text(plain_text: str, key: str) -> str:
    try:
        # Convert the string key to bytes
        aes_key = get_aes_key(key)

        # Generate a random initialization vector (IV)
        iv = get_random_bytes(16)

        # Create an AES cipher object with the given key and IV
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)

        # Pad the plaintext to be a multiple of 16 bytes and encrypt it
        encrypted_bytes = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))

        # Combine IV and encrypted text, then encode it as base64
        encrypted_text = base64.b64encode(iv + encrypted_bytes).decode('utf-8')

        return encrypted_text
    except Exception as e:
        print(e)
        return None


def decrypt_text(encrypted_text: str, key: str) -> str:
    try:
        # Convert the string key to bytes
        aes_key = get_aes_key(key)

        # Decode the base64 encoded string to get the IV + encrypted bytes
        encrypted_bytes = base64.b64decode(encrypted_text)

        # Extract the IV from the first 16 bytes
        iv = encrypted_bytes[:16]

        # Create a new AES cipher object with the same key and extracted IV
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)

        # Decrypt and unpad the text
        decrypted_text = unpad(cipher.decrypt(encrypted_bytes[16:]), AES.block_size).decode('utf-8')

        return decrypted_text
    except:
        return None
