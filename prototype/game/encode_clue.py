'''
#ChatGPT
POC code to take a JSON object containing our selected "card" and encode it
+ embed the CRC value and then encrypt it using a provided private key

Encoding + Encryption w/Private key would take place as part of the badge build process.

The public key is then seeded to the user's badge which can decrypt the card it has
and those it recieves.

MAKE SURE THE PRIVATE/PUBLIC KEY PAIR ARE DIFFERENT THAN THE CLUE PAIR!
'''
import json
import binascii
import zlib
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding

def json_to_hex(json_obj: dict, public_key: rsa.RSAPublicKey) -> str:
    # Convert the JSON object to a string
    json_str = json.dumps(json_obj)

    # Compute the CRC value of the JSON string
    crc = zlib.crc32(json_str.encode())

    # Concatenate the JSON string and the CRC value, and encode them as bytes
    json_crc = (json_str + str(crc)).encode()

    # Encrypt the bytes using the public key
    encrypted_json_crc = public_key.encrypt(json_crc, rsa.padding.OAEP(mgf=rsa.padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

    # Return the base64 encoding of the encrypted bytes
    return base64.b64encode(encrypted_json_crc).decode()

def hex_to_json(hexcode: str, private_key: rsa.RSAPrivateKey) -> dict:
    # Decode the base64-encoded hexcode
    encrypted_json_crc = base64.b64decode(hexcode)

    # Decrypt the encrypted bytes using the private key
    json_crc = private_key.decrypt(encrypted_json_crc, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

    # Split the JSON string and the CRC value
    json_str, crc = json_crc.split(b'\x00')

    # Compute the CRC value of the JSON string
    computed_crc = zlib.crc32(json_str)

    # Check that the computed CRC value matches the stored CRC value
    if crc != computed_crc:
        raise ValueError("CRC check failed")

    # Deserialize the JSON string and return the resulting object
    return json.loads(json_str.decode())

# Example usage
json_obj = {"field1": 123, "field2": "abc"}

# Generate a public/private key pair
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Convert the JSON object to a hexcode
hexcode = json_to_hex(json_obj, public_key)
print(hexcode)

# Convert the hexcode back to a JSON object
json_obj_2 = hex_to_json(hexcode, private_key)
print(json_obj_2)