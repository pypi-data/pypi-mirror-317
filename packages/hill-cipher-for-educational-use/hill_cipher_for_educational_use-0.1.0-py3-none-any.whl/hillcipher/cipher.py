import numpy as np

class HillCipher:
    def __init__(self, block_size=2):
        """
        Initialize the Hill Cipher class.
        :param block_size: Size of encryption blocks (default: 2)
        """
        self.block_size = block_size
        self.key = None

    def generate_key(self):
        """
        Generate an invertible matrix and set it as the key for this instance.
        """
        self.key = self._generate_invertible_matrix(self.block_size)
        print("Generated encryption key (matrix):\n", self.key)
        
    def set_key(self, key):
        """
        Manually set the key for this instance.
        :param key: Encryption key (matrix)
        """
        self.key = np.array(key)
        if not self._is_invertible(self.key):
            raise ValueError("The provided key is not an invertible matrix.")

    def encrypt(self, plaintext):
        """
        Encrypt plaintext using the instance's key.
        :param plaintext: Text to be encrypted
        :return: Ciphertext
        """
        if self.key is None:
            raise ValueError("Encryption key is not set.")
        if not plaintext.isalpha():
            raise ValueError("Plaintext must contain only alphabetic characters.")
        return self._process_text(plaintext, self.key)

    def decrypt(self, ciphertext):
        """
        Decrypt ciphertext using the instance's key.
        :param ciphertext: Text to be decrypted
        :return: Decrypted plaintext
        """
        if self.key is None:
            raise ValueError("Encryption key is not set.")
        inv_key = self._mod_inverse_matrix(self.key)
        return self._process_text(ciphertext, inv_key)

    @classmethod
    def generate_key_matrix(cls, block_size):
        """
        Class method: Generate an invertible matrix of the specified block size.
        :param block_size: Size of the matrix
        :return: Invertible matrix
        """
        return cls._generate_invertible_matrix(block_size)
    
    @classmethod
    def encrypt_with_key(cls, plaintext, key):
        """
        Class method: Encrypt plaintext using the provided key.
        :param plaintext: Text to be encrypted
        :param key: Encryption key (matrix)
        :return: Ciphertext
        """
        if not plaintext.isalpha():
            raise ValueError("Plaintext must contain only alphabetic characters.")
        return cls._process_text(plaintext, key)

    @classmethod
    def decrypt_with_key(cls, ciphertext, key):
        """
        Class method: Decrypt ciphertext using the provided key.
        :param ciphertext: Text to be decrypted
        :param key: Encryption key (matrix)
        :return: Decrypted plaintext
        """
        inv_key = cls._mod_inverse_matrix(key)
        return cls._process_text(ciphertext, inv_key)

    @staticmethod
    def _generate_invertible_matrix(size):
        """
        Generate an invertible matrix of the specified size.
        :param size: Size of the matrix
        :return: Invertible matrix
        """
        while True:
            matrix = np.random.randint(1, 10, (size, size))
            if HillCipher._is_invertible(matrix):
                return matrix

    @staticmethod
    def _is_invertible(matrix, mod=26):
        """
        Check if a matrix is invertible modulo 26.
        :param matrix: Matrix to check
        :param mod: Modulus value (default: 26)
        :return: True if invertible, False otherwise
        """
        det = int(np.round(np.linalg.det(matrix)))
        return np.gcd(det, mod) == 1

    @staticmethod
    def _mod_inverse_matrix(matrix, mod=26):
        """
        Compute the modular inverse of a matrix.
        :param matrix: Original matrix
        :param mod: Modulus value
        :return: Modular inverse of the matrix
        """
        det = int(np.round(np.linalg.det(matrix)))  # Determinant of the matrix
        det_inv = pow(det, -1, mod)  # Modular inverse of the determinant
        adjugate = np.round(det * np.linalg.inv(matrix)).astype(int) % mod  # Adjugate matrix
        return (det_inv * adjugate) % mod

    @staticmethod
    def _process_text(text, matrix):
        """
        Process plaintext or ciphertext in blocks.
        :param text: Text to process
        :param matrix: Matrix to use for processing
        :return: Processed text
        """
        block_size = matrix.shape[0]
        text = text.upper().replace(" ", "")  # Convert to uppercase and remove spaces
        padding_length = (-len(text)) % block_size
        text += 'X' * padding_length  # Add padding if needed
        blocks = [text[i:i + block_size] for i in range(0, len(text), block_size)]
        result_blocks = []
        for block in blocks:
            vector = np.array([ord(char) - 65 for char in block])  # Convert characters to numbers (A=0, B=1, ...)
            result_vector = np.dot(matrix, vector) % 26
            result_blocks.append(''.join(chr(c + 65) for c in result_vector))
        return ''.join(result_blocks)
    
    def explain_encryption(self, plaintext):
        """
        Explain the encryption process step by step.
        :param plaintext: The plaintext to encrypt.
        :return: The resulting ciphertext.
        """
        if self.key is None:
            raise ValueError("Encryption key is not set.")
        
        print("=== Hill Cipher Encryption Process ===")
        
        # Step 1: Preprocess the plaintext
        print("\nStep 1: Convert plaintext to uppercase and remove spaces.")
        text = plaintext.upper().replace(" ", "")
        print(f"Processed plaintext: {text}")

        # Step 2: Add padding if necessary
        block_size = self.key.shape[0]
        padding_length = (-len(text)) % block_size
        text += 'X' * padding_length
        print(f"After padding (block size = {block_size}): {text}")
        
        # Step 3: Break plaintext into blocks
        print("\nStep 2: Divide plaintext into blocks of size:", block_size)
        blocks = [text[i:i + block_size] for i in range(0, len(text), block_size)]
        print(f"Blocks: {blocks}")

        # Step 4: Convert each block to a vector and apply matrix multiplication
        print("\nStep 3: Convert each block to a numerical vector and apply key matrix multiplication.")
        result_blocks = []
        for block in blocks:
            vector = [ord(char) - 65 for char in block]  # Convert letters to numbers
            print(f"\nBlock '{block}' as vector: {vector}")
            result_vector = np.dot(self.key, vector) % 26
            print(f"Resulting vector after key multiplication: {result_vector}")
            encrypted_block = ''.join(chr(num + 65) for num in result_vector)
            print(f"Encrypted block: {encrypted_block}")
            result_blocks.append(encrypted_block)
        
        # Step 5: Combine the encrypted blocks into the final ciphertext
        ciphertext = ''.join(result_blocks)
        print("\nStep 4: Combine all encrypted blocks to form the ciphertext.")
        print(f"Ciphertext: {ciphertext}")
        return ciphertext

    def explain_decryption(self, ciphertext):
        """
        Explain the decryption process step by step.
        :param ciphertext: The ciphertext to decrypt.
        :return: The resulting plaintext.
        """
        if self.key is None:
            raise ValueError("Encryption key is not set.")
        
        print("=== Hill Cipher Decryption Process ===")

        # Step 1: Calculate the inverse of the key matrix
        print("\nStep 1: Calculate the modular inverse of the key matrix.")
        inv_key = self._mod_inverse_matrix(self.key)
        print(f"Inverse key matrix (mod 26):\n{inv_key}")

        # Step 2: Divide ciphertext into blocks
        block_size = self.key.shape[0]
        print("\nStep 2: Divide ciphertext into blocks of size:", block_size)
        blocks = [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]
        print(f"Blocks: {blocks}")

        # Step 3: Convert each block to a vector and apply inverse key multiplication
        print("\nStep 3: Convert each block to a numerical vector and apply inverse key matrix multiplication.")
        result_blocks = []
        for block in blocks:
            vector = [ord(char) - 65 for char in block]  # Convert letters to numbers
            print(f"\nBlock '{block}' as vector: {vector}")
            result_vector = np.dot(inv_key, vector) % 26
            result_vector = np.round(result_vector).astype(int) % 26  # Ensure rounding and mod 26
            print(f"Resulting vector after inverse key multiplication: {result_vector}")
            decrypted_block = ''.join(chr(num + 65) for num in result_vector)
            print(f"Decrypted block: {decrypted_block}")
            result_blocks.append(decrypted_block)
        
        # Step 4: Combine the decrypted blocks into the final plaintext
        plaintext = ''.join(result_blocks)
        print("\nStep 4: Combine all decrypted blocks to form the plaintext.")
        print(f"Plaintext: {plaintext}")
        return plaintext

# Example usage
if __name__ == "__main__":
    # Using class methods
    block_size = 2
    key = HillCipher.generate_key(block_size)  # Generate key using class method
    print("Generated key (class method):\n", key)

    plaintext = "HELLO"
    ciphertext = HillCipher.encrypt(plaintext, key)  # Encrypt using class method
    print("Ciphertext (class method):", ciphertext)

    decrypted = HillCipher.decrypt(ciphertext, key)  # Decrypt using class method
    print("Decrypted text (class method):", decrypted)

    # Using instance methods
    cipher = HillCipher(block_size=2)
    cipher.generate_key()  # Generate key using instance method
    ciphertext_instance = cipher.encrypt(plaintext)  # Encrypt using instance method
    print("Ciphertext (instance method):", ciphertext_instance)
    decrypted_instance = cipher.decrypt(ciphertext_instance)  # Decrypt using instance method
    print("Decrypted text (instance method):", decrypted_instance)