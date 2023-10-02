import argparse

class PlayfairCipher:
    """This class implements the Playfair Cipher encryption and decryption."""
    def __init__(self, key):
        """
        Initialize the PlayfairCipher instance with a given key.

        Args:
            key (str): The encryption key.
        """
        self.key = ''.join(sorted(set(key.upper()), key=lambda x: key.lower().index(x)))
        self.key_matrix = [self.key[i:i + 5] for i in range(0, len(self.key), 5)]
        self.alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    def find_positions(self, char):
        """
        Find the row and column positions of a character in the key matrix.

        Args:
            char (str): The character to find in the key matrix.

        Returns:
            Tuple[int, int]: The row and column positions of the character.
        """
        for row_idx, row in enumerate(self.key_matrix):
            if char in row:
                return row_idx, row.index(char)
        return None, None

    def process_text(self, text):
        """
        Process the input text by removing non-alphabetic characters and making it uppercase.

        Args:
            text (str): The input text.

        Returns:
            str: The processed text.
        """
        text = ''.join([c.upper() for c in text if c.isalpha()])
        if len(text) % 2 == 1:
            text += 'X'
        return text

    def transform(self, text, mode):
        """
        Encrypt or decrypt the input text using the Playfair Cipher.

        Args:
            text (str): The input text.
            mode (str): The encryption/decryption mode ("encrypt" or "decrypt").

        Returns:
            str: The encrypted or decrypted text.
        """
        text = self.process_text(text)
        result = ""
        for i in range(0, len(text), 2):
            char1, char2 = text[i], text[i + 1]
            row1, col1 = self.find_positions(char1)
            row2, col2 = self.find_positions(char2)

            if row1 == row2:
                col1, col2 = (col1 + 1) % 5, (col2 + 1) % 5
            elif col1 == col2:
                row1, row2 = (row1 + 1) % 5, (row2 + 1) % 5
            else:
                col1, col2 = col2, col1

            if mode == "encrypt":
                result += self.key_matrix[row1][col1] + self.key_matrix[row2][col2]
            else:
                result += self.key_matrix[row1][col1] + self.key_matrix[row2][col2]

        return result

class RailFence:
    """This class implements the Rail Fence Cipher encryption and decryption."""
    def __init__(self, rails=2):
        """
        Initialize the RailFence instance with the number of rails.

        Args:
            rails (int): The number of rails in the Rail Fence Cipher (default is 2).
        """
        self.rails = rails

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using the Rail Fence Cipher.

        Args:
            plaintext (str): The plaintext to encrypt.

        Returns:
            str: The encrypted ciphertext.
        """
        fence = [[' ' for _ in plaintext] for _ in range(self.rails)]
        rail, direction = 0, 1

        for char in plaintext:
            fence[rail][len(fence[rail]) - len(plaintext)] = char
            rail += direction
            if rail == self.rails - 1 or rail == 0:
                direction *= -1

        return ''.join([''.join(row) for row in fence])

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using the Rail Fence Cipher.

        Args:
            ciphertext (str): The ciphertext to decrypt.

        Returns:
            str: The decrypted plaintext.
        """
        fence = [[' ' for _ in ciphertext] for _ in range(self.rails)]
        rail, direction, plaintext = 0, 1, ''

        for _ in range(len(fence[0])):
            plaintext += fence[rail][0]
            rail += direction
            if rail == self.rails - 1 or rail == 0:
                direction *= -1
            fence[rail][0] = ' '

        return plaintext

class Substitution:
    """This class implements the Substitution Cipher encryption and decryption."""
    def __init__(self, password):
        """
        Initialize the Substitution instance with a password.

        Args:
            password (str): The password used for creating the substitution key.
        """
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.key = "".join(sorted(set(password.lower().replace(" ", "")), key=lambda x: password.lower().index(x)) + [ch for ch in self.alphabet if ch not in password])

    def transform(self, text, mode):
        """
        Encrypt or decrypt the input text using the Substitution Cipher.

        Args:
            text (str): The input text.
            mode (str): The encryption/decryption mode ("encrypt" or "decrypt").

        Returns:
            str: The encrypted or decrypted text.
        """
        result = ""
        for ch in text:
            result += self.key[self.alphabet.index(ch)] if ch in self.alphabet else ch
        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encryption/Decryption using various ciphers")
    parser.add_argument("-a", "--algorithm", choices=["Playfair", "RailFence", "Substitution"], required=True, help="Encryption algorithm")
    parser.add_argument("-k", "--key", required=True, help="Encryption key")
    parser.add_argument("-t", "--text", required=True, help="Text to encrypt/decrypt")
    parser.add_argument("-m", "--mode", choices=["encrypt", "decrypt"], required=True, help="Encryption/decryption mode")

    args = parser.parse_args()

    if args.algorithm == "Playfair":
        cipher = PlayfairCipher(args.key)
    elif args.algorithm == "RailFence":
        cipher = RailFence()
    elif args.algorithm == "Substitution":
        cipher = Substitution(args.key)

    result = cipher.transform(args.text, args.mode)
    print(result)


