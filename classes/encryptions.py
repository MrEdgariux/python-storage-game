import win32crypt
import json

class WindowsHelloEncryptor:
    @staticmethod
    def encrypt_save(data, save_path):
        """Encrypts the save file using Windows Hello/DPAPI."""
        # Convert data to JSON string and encode it to bytes
        data_bytes = json.dumps(data).encode()

        # Encrypt using DPAPI for the current user (CRYPTPROTECT_UI_FORBIDDEN prevents UI prompts)
        try:
            encrypted_data = win32crypt.CryptProtectData(
                data_bytes, None, None, None, None, 0
            )
        except Exception as e:
            raise ValueError("Prašome įsijungti Windows Hello naxui!")

        # Write encrypted data to file
        with open(save_path, "wb") as f:
            f.write(encrypted_data)
    
    @staticmethod
    def decrypt_save(save_path):
        """Decrypts the save file using Windows Hello/DPAPI."""
        with open(save_path, "rb") as f:
            encrypted_data = f.read()

        # Decrypt using DPAPI for the current user
        try:
            decrypted_data = win32crypt.CryptUnprotectData(
                encrypted_data, None, None, None, 0
            )[1]
        except Exception as e:
            raise ValueError("We could not decrypt this file, if you are not the owner of this file, you cannot decrypt it you peace of garbage!")

        # Convert bytes back to JSON and return Python dictionary
        return json.loads(decrypted_data.decode())