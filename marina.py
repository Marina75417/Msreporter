#!/usr/bin/env python3
# MARINA KHAN'S FILE CRYPT - AES-256 ENCRYPTION/DECRYPTION
import os
import sys
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
import argparse
import base64

class MarinaCrypt:
    HEADER = """
    ╔══════════════════════════════════════════╗
    ║    MARINA KHAN'S FILE CRYPT v1.0        ║
    ║    • AES-256 Encryption                 ║
    ║    • Secure Key Derivation              ║
    ║    • Tamper Detection                   ║
    ╚══════════════════════════════════════════╝
    """
    
    SALT_SIZE = 16
    NONCE_SIZE = 12  # GCM recommended nonce size
    TAG_SIZE = 16    # GCM authentication tag
    SCRYPT_PARAMS = {
        "N": 2**14,  # CPU/memory cost
        "r": 8,      # Block size
        "p": 1       # Parallelization
    }

    def __init__(self):
        print(self.HEADER)
        self._setup_args()

    def _setup_args(self):
        self.parser = argparse.ArgumentParser(
            description="MARINA KHAN'S FILE ENCRYPTION TOOL",
            epilog="Example: ./marina_crypt.py encrypt secret.txt -o encrypted.marina"
        )
        subparsers = self.parser.add_subparsers(dest='command', required=True)

        # Encrypt command
        enc_parser = subparsers.add_parser('encrypt', help='Encrypt a file')
        enc_parser.add_argument('input', help='File to encrypt')
        enc_parser.add_argument('-o', '--output', help='Output file')
        enc_parser.add_argument('-k', '--key', help='Custom encryption key (optional)')

        # Decrypt command
        dec_parser = subparsers.add_parser('decrypt', help='Decrypt a file')
        dec_parser.add_argument('input', help='File to decrypt')
        dec_parser.add_argument('-o', '--output', help='Output file')

    def _derive_key(self, password, salt):
        """Generate 256-bit key using scrypt KDF"""
        return scrypt(
            password.encode(), 
            salt, 
            key_len=32, 
            N=self.SCRYPT_PARAMS["N"],
            r=self.SCRYPT_PARAMS["r"],
            p=self.SCRYPT_PARAMS["p"]
        )

    def encrypt_file(self, input_path, output_path=None, key=None):
        """Encrypt file with AES-256-GCM"""
        if not output_path:
            output_path = input_path + ".marina"

        salt = get_random_bytes(self.SALT_SIZE)
        nonce = get_random_bytes(self.NONCE_SIZE)

        # Get encryption key
        if not key:
            key = input("Enter encryption key: ")
        enc_key = self._derive_key(key, salt)

        cipher = AES.new(enc_key, AES.MODE_GCM, nonce=nonce)
        
        with open(input_path, 'rb') as f_in:
            plaintext = f_in.read()
            ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        with open(output_path, 'wb') as f_out:
            [f_out.write(x) for x in (salt, nonce, tag, ciphertext)]

        print(f"✅ ENCRYPTED: {input_path} → {output_path}")
        print(f"🔑 Key: {key if len(key) < 20 else key[:10]+'...'+key[-5:]}")
        return True

    def decrypt_file(self, input_path, output_path=None, key=None):
        """Decrypt file with AES-256-GCM"""
        if not output_path:
            if input_path.endswith('.marina'):
                output_path = input_path[:-7]
            else:
                output_path = input_path + ".decrypted"

        with open(input_path, 'rb') as f_in:
            salt = f_in.read(self.SALT_SIZE)
            nonce = f_in.read(self.NONCE_SIZE)
            tag = f_in.read(self.TAG_SIZE)
            ciphertext = f_in.read()

        if not key:
            key = input("Enter decryption key: ")
        dec_key = self._derive_key(key, salt)

        try:
            cipher = AES.new(dec_key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            
            with open(output_path, 'wb') as f_out:
                f_out.write(plaintext)

            print(f"✅ DECRYPTED: {input_path} → {output_path}")
            return True
        except ValueError as e:
            print(f"❌ DECRYPTION FAILED: {str(e)}")
            return False

    def run(self):
        args = self.parser.parse_args()

        if args.command == 'encrypt':
            self.encrypt_file(args.input, args.output, args.key)
        elif args.command == 'decrypt':
            self.decrypt_file(args.input, args.output, args.key)

if __name__ == "__main__":
    tool = MarinaCrypt()
    tool.run()
