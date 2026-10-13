import os

KEY_FILE = "secret.key"

# Generate Secret Key
def generate_key():
    key = os.urandom(32)  # 32 bytes random key
    with open(KEY_FILE, "wb") as file:
        file.write(key)
    print("\n✅ Secret key generated successfully!")
    print("Keep secret.key safe.")

# Load Secret Key
def load_key():
    if not os.path.exists(KEY_FILE):
        print("\n❌ Secret key not found! Generate a key first.")
        return None
    with open(KEY_FILE, "rb") as file:
        return file.read()

# XOR Encrypt/Decrypt
def xor_data(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

# Encrypt File
def encrypt_file():
    path = input("\nEnter file path to encrypt: ").strip()
    if not os.path.isfile(path):
        print("❌ Error: File not found!")
        return

    key = load_key()
    if key is None:
        return

    try:
        with open(path, "rb") as file:
            data = file.read()

        encrypted = xor_data(data, key)
        output = path + ".encrypted"

        with open(output, "wb") as file:
            file.write(encrypted)

        print("\n🔒 File encrypted successfully!")
        print("Saved as:", output)

    except Exception as error:
        print("❌ Error:", error)

# Decrypt File
def decrypt_file():
    path = input("\nEnter encrypted file path: ").strip()
    if not os.path.isfile(path):
        print("❌ Error: File not found!")
        return

    key = load_key()
    if key is None:
        return

    try:
        with open(path, "rb") as file:
            data = file.read()

        decrypted = xor_data(data, key)

        if path.endswith(".encrypted"):
            output = path[:-10]
        else:
            output = path + ".decrypted"

        # Avoid overwriting existing file
        if os.path.exists(output):
            output += ".decrypted"

        with open(output, "wb") as file:
            file.write(decrypted)

        print("\n🔓 File decrypted successfully!")
        print("Saved as:", output)

    except Exception as error:
        print("❌ Error:", error)

# Main Menu
def main():
    while True:
        print("\n" + "=" * 40)
        print("     FILE ENCRYPTION TOOL (XOR)")
        print("=" * 40)
        print("1. Generate Secret Key")
        print("2. Encrypt File")
        print("3. Decrypt File")
        print("4. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            generate_key()
        elif choice == "2":
            encrypt_file()
        elif choice == "3":
            decrypt_file()
        elif choice == "4":
            print("👋 Thank you for using the tool!")
            break
        else:
            print("⚠️ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
