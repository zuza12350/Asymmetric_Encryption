"""
    Authors:
    Zuzanna Borkowska (s21243)
    Aleksnader Mazurek (s15023)
"""
import glob
import re
from Cryptodome.Random import get_random_bytes
from secrets import token_bytes
from  aes_en import AESCipher
from  des import DESCipher
from  des3 import DES3Cipher
from rsa_en import RSACipher
from config import Config
from hashlib import md5
import random
import hashlib



def main():
    pass


option = input('Select symmetric and asymmetric algorithm \n1-AES and RES\n2-DES and RES\n3-DES3 and RES\n4-AES and Diffie-Helman\n5-DES and Diffie-Helman\n6-DES3 and Diffie-Helman ')
"""
 The user has a choice of options:
  1: AES and RES
  2: DES and RES
  3: DES3 and RES 
  4: AES and Diffie-Helman 
  5: DES and Diffie-Helman 
  6: DES3 and Diffie-Helman 
"""
if __name__ == '__main__':
    if option == '1':
        """
        Random key generation for aes
        """
        aes_key = get_random_bytes(16)
        aes_cipher = AESCipher(aes_key)
        rsa_cipher = RSACipher()
        while True:
            choice = input('Do you want ?\n 1- encrypt \n 2- decrypt \n 3- exit \nfiles?:\n')
            """
                    The user has a choice of options:
                    1: encrypting all files 
                    2: decrypt encrypted files
                    3: terminate the process
                """
            if choice == '3':
                exit(0)
            if choice == '1':
                for file in glob.glob("test/*.txt"):
                    with open(file, "r+") as f:
                        """
                        Data encryption 
                        """
                        encrypt_text = aes_cipher.encrypt(f.read())
                        f.seek(0)
                        f.write(encrypt_text)
            if choice == '2':
                """
                Signing aes keys with customer's private key
                """
                signature = rsa_cipher.sign(Config.CLIENT_PRIVATE_KEY, aes_key)
                """
                Encrypt aes key using server-side public key
                """
                encrypt_key = rsa_cipher.encrypt(Config.SERVER_PUBLIC_KEY, aes_key)
                """
                Decrypt the encrypted aes key using the server-side private key
                """
                aes_key = rsa_cipher.decrypt(Config.SERVER_PRIVATE_KEY, encrypt_key)
                """
                Use client-side public key to verify signatures
                """
                result = rsa_cipher.verify(Config.CLIENT_PUBLIC_KEY, aes_key, signature)
                for file in glob.glob("test/*.txt"):
                    with open(file, "r+") as f:
                        """
                        Decrypt the cipher text with aes
                        """
                        aes_cipher = AESCipher(aes_key)
                        decrypt_text = aes_cipher.decrypt(f.read())
                        f.truncate()
                        f.write(decrypt_text)
    if option == '2':
        ciphertext_tab = []
        nonce_tab = []
        tag_tab = []
        des_key = token_bytes(8)
        des_cipher = DESCipher(des_key)
        rsa_cipher = RSACipher()
        while True:
            choice = input('Do you want ?\n 1- encrypt \n 2- decrypt \n 3- exit \nfiles?: ')
            """
                    The user has a choice of options:
                    1: encrypting all files 
                    2: decrypt encrypted files
                    3: terminate the process
                """
            if choice == '3':
                exit(0)
            if choice == '1':
                for file in glob.glob("test/*.txt"):
                    with open(file, "r+") as f:
                        """
                            Data encryption 
                        """
                        nonce, encrypt_text, tag  = des_cipher.encrypt(f.read())
                        ciphertext_tab.append(encrypt_text)
                        nonce_tab.append(nonce)
                        tag_tab.append(tag)
                        f.seek(0)
                        f.write(re.sub('[^a-zA-Z0-9 \n\.]', '', encrypt_text.__str__()))

            if choice == '2':
                """
                   Signing des keys with customer's private key
                """
                signature = rsa_cipher.sign(Config.CLIENT_PRIVATE_KEY, des_key)
                """
                  Encrypt des key using server-side public key
                """
                encrypt_key = rsa_cipher.encrypt(Config.SERVER_PUBLIC_KEY, des_key)
                """
                Decrypt the encrypted des key using the server-side private key
                """
                des_key = rsa_cipher.decrypt(Config.SERVER_PRIVATE_KEY, encrypt_key)
                """
                Use client-side public key to verify signatures
                """
                result = rsa_cipher.verify(Config.CLIENT_PUBLIC_KEY, des_key, signature)
                des_cipher = DESCipher(des_key)
                i = 0
                for file in glob.glob("test/*.txt"):
                    with open(file, "r+") as f:
                        """
                        Data decryption
                        """
                        nonce = nonce_tab[i]
                        tag = tag_tab[i]
                        ciphertext = ciphertext_tab[i]
                        plaintext = des_cipher.decrypt(nonce, ciphertext, tag)
                        f.truncate()
                        f.write(plaintext)
                        i += 1
    if option == '3':
        """
           Passing key to DES3Ciper class
         """
        key = "test_passkey"
        des3_key = md5(key.encode('ascii')).digest()
        des3_cipher = DES3Cipher(des3_key)
        rsa_cipher = RSACipher()
        while True:
            choice = input('Do you want ?\n 1- encrypt \n 2- decrypt \n 3- exit \nfiles?: ')
            """
                    The user has a choice of options:
                    1: encrypting all files 
                    2: decrypt encrypted files
                    3: terminate the process
                """
            if choice == '3':
                exit(0)
            if choice == '1':
                for file in glob.glob("test/*.txt"):
                        """
                        Data encryption 
                        """
                        encrypt_text = des3_cipher.encryptall(file)
            if choice == '2':
                """
                Signing des3 keys with customer's private key
                """
                signature = rsa_cipher.sign(Config.CLIENT_PRIVATE_KEY, des3_key)
                """
                Encrypt des3 key using server-side public key
                """
                encrypt_key = rsa_cipher.encrypt(Config.SERVER_PUBLIC_KEY, des3_key)
                """
                Decrypt the encrypted des3 key using the server-side private key
                """
                des3_key = rsa_cipher.decrypt(Config.SERVER_PRIVATE_KEY, encrypt_key)
                """
                Use client-side public key to verify signatures
                """
                result = rsa_cipher.verify(Config.CLIENT_PUBLIC_KEY, des3_key, signature)
                for file in glob.glob("test/*.txt"):
                        """
                         Data decryption 
                        """
                        des3_cipher = DES3Cipher(des3_key)
                        decrypt_text = des3_cipher.descryptall(file)
    if option == '4':
        """        
        Random key generation for aes
        """
        aes_key = get_random_bytes(16)
        aes_cipher = AESCipher(aes_key)
        while True:
            """
            B key generating function
            """
            def KeyB(A, b, p):
                key_bb = (A ** b) % p
                retB = hashlib.sha256(str(key_bb).encode()).hexdigest()
                return retB
            """
            A key generating function
            """
            def KeyA(B, a, p):
                key_aa = (B ** a) % p
                retA = hashlib.sha256(str(key_aa).encode()).hexdigest()
                return retA


            choice = input('Do you want ?\n 1- encrypt \n 2- decrypt \n 3- exit \nfiles?: ')
            """
                    The user has a choice of options:
                    1: encrypting all files 
                    2: decrypt encrypted files
                    3: terminate the process
                """
            if choice == '3':
                exit(0)
            if choice == '1':
                p = int(input("Shared value: "))
                g = int(input("Pirme number: "))
                """b = Bob random value"""
                b = random.randint(10, 20)
                """a = Alice random value"""
                a = random.randint(5, 10)
                """A =  Alice value (g^a) mod p"""
                A = (g ** a) % p
                """B = Bob value (g^b) mod p"""
                B = (g ** b) % p
                alice = str(KeyA(B, a, p))
                print(alice)
                """
                It is necessary to remove the variables for later computation of the key B (Bob) for decrytion
                """
                del p
                del g
                del A
                del B
                for file in glob.glob("test/*.txt"):
                    with open(file, "r+") as f:
                        """
                        Data encryption 
                        """
                        encrypt_text = aes_cipher.encrypt(f.read())
                        f.seek(0)
                        f.write(encrypt_text)
            if choice == '2':
                p = int(input("shared value :"))
                g = int(input("pirme number: "))
                """A =  Alice value (g^a) mod p"""
                A = (g ** a) % p
                """B = Bob value (g^b) mod p"""
                B = (g ** b) % p
                bob = str(KeyB(A, b, p))
                print(bob)
                if bob == alice:
                    for file in glob.glob("test/*.txt"):
                        with open(file, "r+") as f:
                            """
                            Decrypt the cipher text with aes
                            """
                            aes_cipher = AESCipher(aes_key)
                            decrypt_text = aes_cipher.decrypt(f.read())
                            f.truncate()
                            f.write(decrypt_text)
                else:
                    print("Wrong values!")
                    p = int(input("Shared value: "))
                    g = int(input("Pirme number: "))
                    """A =  Alice value (g^a) mod p"""
                    A = (g ** a) % p
                    """B = Bob value (g^b) mod p"""
                    bob = str(KeyB(A, b, p))
                    if bob == alice:
                        for file in glob.glob("test/*.txt"):
                            with open(file, "r+") as f:
                                """
                                Decrypt the cipher text with aes
                                """
                                aes_cipher = AESCipher(aes_key)
                                decrypt_text = aes_cipher.decrypt(f.read())
                                f.truncate()
                                f.write(decrypt_text)
                    else:
                        break
    if option == '5':
        ciphertext_tab = []
        nonce_tab = []
        tag_tab = []
        des_key = token_bytes(8)
        des_cipher = DESCipher(des_key)
        while True:
            """
            B key generating function
            """
            def KeyB(A, b, p):
                key_bb = (A ** b) % p
                retB = hashlib.sha256(str(key_bb).encode()).hexdigest()
                return retB
            """
            A key generating function
            """
            def KeyA(B, a, p):
                key_aa = (B ** a) % p
                retA = hashlib.sha256(str(key_aa).encode()).hexdigest()
                return retA


            choice = input('Do you want ?\n 1- encrypt \n 2- decrypt \n 3- exit \nfiles?: ')
            """
                    The user has a choice of options:
                    1: encrypting all files 
                    2: decrypt encrypted files
                    3: terminate the process
                """
            if choice == '3':
                exit(0)
            if choice == '1':
                p = int(input("Shared value: "))
                g = int(input("Pirme number: "))
                """b = Bob random value"""
                b = random.randint(10, 20)
                """a = Alice random value"""
                a = random.randint(5, 10)
                """A =  Alice value (g^a) mod p"""
                A = (g ** a) % p
                """B = Bob value (g^b) mod p"""
                B = (g ** b) % p
                alice = str(KeyA(B, a, p))
                print(alice)
                """
                It is necessary to remove the variables for later computation of the key B (Bob) for decrytion
                """
                del p
                del g
                del A
                del B
                for file in glob.glob("test/*.txt"):
                    with open(file, "r+") as f:
                        """
                            Data encryption 
                        """
                        nonce, encrypt_text, tag = des_cipher.encrypt(f.read())
                        ciphertext_tab.append(encrypt_text)
                        nonce_tab.append(nonce)
                        tag_tab.append(tag)
                        f.seek(0)
                        f.write(re.sub('[^a-zA-Z0-9 \n\.]', '', encrypt_text.__str__()))

            if choice == '2':

                p = int(input("shared value :"))
                g = int(input("pirme number: "))
                """A =  Alice value (g^a) mod p"""
                A = (g ** a) % p
                """B = Bob value (g^b) mod p"""
                B = (g ** b) % p
                bob = str(KeyB(A, b, p))
                print(bob)
                if bob == alice:
                    i = 0
                    for file in glob.glob("test/*.txt"):
                        with open(file, "r+") as f:
                            """
                            Data decryption
                            """
                            nonce = nonce_tab[i]
                            tag = tag_tab[i]
                            ciphertext = ciphertext_tab[i]
                            plaintext = des_cipher.decrypt(nonce, ciphertext, tag)
                            f.truncate()
                            f.write(plaintext)
                            i += 1
                else:
                    print("Wrong values!")
                    p = int(input("Shared value: "))
                    g = int(input("Pirme number: "))
                    """A =  Alice value (g^a) mod p"""
                    A = (g ** a) % p
                    """B = Bob value (g^b) mod p"""
                    B = (g ** b) % p
                    bob = str(KeyB(A, b, p))
                    if bob == alice:
                        i = 0
                        for file in glob.glob("test/*.txt"):
                            with open(file, "r+") as f:
                                """
                                Data decryption
                                """
                                nonce = nonce_tab[i]
                                tag = tag_tab[i]
                                ciphertext = ciphertext_tab[i]
                                plaintext = des_cipher.decrypt(nonce, ciphertext, tag)
                                f.truncate()
                                f.write(plaintext)
                                i += 1
                    else:
                        break
    if option == '6':
        key = "test_passkey"
        des3_key = md5(key.encode('ascii')).digest()
        des3_cipher = DES3Cipher(des3_key)

        while True:
            """
            B key generating function
            """
            def KeyB(A, b, p):
                key_bb = (A ** b) % p
                retB = hashlib.sha256(str(key_bb).encode()).hexdigest()
                return retB
            """
            A key generating function
            """
            def KeyA(B, a, p):
                key_aa = (B ** a) % p
                retA = hashlib.sha256(str(key_aa).encode()).hexdigest()
                return retA


            choice = input('Do you want ?\n 1- encrypt \n 2- decrypt \n 3- exit \nfiles?: ')
            """
                    The user has a choice of options:
                    1: encrypting all files 
                    2: decrypt encrypted files
                    3: terminate the process
                """
            if choice == '3':
                exit(0)
            if choice == '1':
                p = int(input("Shared value: "))
                g = int(input("Pirme number: "))
                """b = Bob random value"""
                b = random.randint(10, 20)
                """a = Alice random value"""
                a = random.randint(5, 10)
                """A =  Alice value (g^a) mod p"""
                A = (g ** a) % p
                """B = Bob value (g^b) mod p"""
                B = (g ** b) % p
                alice = str(KeyA(B, a, p))
                print(alice)
                """
                It is necessary to remove the variables for later computation of the key B (Bob) for decrytion
                """
                del p
                del g
                del A
                del B
                for file in glob.glob("test/*.txt"):
                    """
                    Data encryption 
                    """
                    encrypt_text = des3_cipher.encryptall(file)
            if choice == '2':

                p = int(input("shared value :"))
                g = int(input("pirme number: "))
                """A =  Alice value (g^a) mod p"""
                A = (g ** a) % p
                """B = Bob value (g^b) mod p"""
                B = (g ** b) % p
                bob = str(KeyB(A, b, p))
                print(bob)

                if bob == alice:
                    for file in glob.glob("test/*.txt"):
                        """
                         Data decryption 
                        """
                        des3_cipher = DES3Cipher(des3_key)
                        decrypt_text = des3_cipher.descryptall(file)
                else:
                    print("Wrong values!")
                    p = int(input("shared value : "))
                    g = int(input("pirme number: "))
                    """A =  Alice value (g^a) mod p"""
                    A = (g ** a) % p
                    """B = Bob value (g^b) mod p"""
                    B = (g ** b) % p
                    bob = str(KeyB(A, b, p))
                    if bob == alice:
                        for file in glob.glob("test/*.txt"):
                            """
                             Data decryption 
                            """
                            des3_cipher = DES3Cipher(des3_key)
                            decrypt_text = des3_cipher.descryptall(file)
                    else:
                        break
