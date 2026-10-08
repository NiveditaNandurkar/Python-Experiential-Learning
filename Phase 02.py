import os
import tkinter as tk
from tkinter import filedialog, messagebox


KEY_FILE = "secret.key"


# ---------------- KEY GENERATION (Phase 1) ----------------

def generate_key():
    key = os.urandom(32)

    with open(KEY_FILE, "wb") as file:
        file.write(key)

    messagebox.showinfo(
        "Success",
        "Secret key generated successfully!\n\n"
        "Keep secret.key safe."
    )


# ---------------- LOAD KEY (Phase 1) ----------------

def load_key():
    if not os.path.exists(KEY_FILE):
        messagebox.showerror(
            "Error",
            "secret.key not found!\nPlease generate a key first."
        )
        return None

    with open(KEY_FILE, "rb") as file:
        return file.read()


# ---------------- XOR FUNCTION (Phase 2) ----------------

def xor_data(data, key):
    result = bytearray()

    for i in range(len(data)):
        result.append(data[i] ^ key[i % len(key)])

    return bytes(result)


# ---------------- ENCRYPT FILE (Phase 2) ----------------

def encrypt_file():

    file_path = filedialog.askopenfilename(
        title="Select File to Encrypt"
    )

    if not file_path:
        return

    key = load_key()

    if key is None:
        return

    try:
        with open(file_path, "rb") as file:
            data = file.read()

        encrypted_data = xor_data(data, key)

        encrypted_file = file_path + ".encrypted"

        with open(encrypted_file, "wb") as file:
            file.write(encrypted_data)

        messagebox.showinfo(
            "Encryption Successful",
            "File encrypted successfully!\n\n"
            f"Saved as:\n{encrypted_file}"
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


# ---------------- DECRYPT FILE (Phase 2) ----------------

def decrypt_file():

    file_path = filedialog.askopenfilename(
        title="Select Encrypted File",
        filetypes=[
            ("Encrypted Files", "*.encrypted"),
            ("All Files", "*.*")
        ]
    )

    if not file_path:
        return

    key = load_key()

    if key is None:
        return

    try:
        with open(file_path, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = xor_data(
            encrypted_data,
            key
        )

        if file_path.endswith(".encrypted"):
            decrypted_file = file_path[:-10]
        else:
            decrypted_file = file_path + ".decrypted"

        with open(decrypted_file, "wb") as file:
            file.write(decrypted_data)

        messagebox.showinfo(
            "Decryption Successful",
            "File decrypted successfully!\n\n"
            f"Saved as:\n{decrypted_file}"
        )

    except Exception as e:
        messagebox.showerror(
            "Decryption Error",
            str(e)
        )


# ---------------- GUI ----------------

root = tk.Tk()

root.title("File Encryption & Decryption Tool")
root.geometry("550x450")
root.resizable(False, False)

root.configure(bg="#101827")


# Title

title = tk.Label(
    root,
    text="🔐 File Encryption Tool",
    font=("Arial", 24, "bold"),
    fg="white",
    bg="#101827"
)

title.pack(pady=30)


# Subtitle

subtitle = tk.Label(
    root,
    text="Secure your files using a secret key",
    font=("Arial", 12),
    fg="#aeb8c7",
    bg="#101827"
)

subtitle.pack(pady=5)


# Generate Key

key_button = tk.Button(
    root,
    text="🔑 Generate Secret Key",
    command=generate_key,
    font=("Arial", 12, "bold"),
    width=32,
    height=2,
    bg="#2563eb",
    fg="white",
    relief="flat",
    cursor="hand2"
)

key_button.pack(pady=15)


# Encrypt (Phase 2)

encrypt_button = tk.Button(
    root,
    text="🔒 Encrypt File",
    command=encrypt_file,
    font=("Arial", 12, "bold"),
    width=32,
    height=2,
    bg="#16a34a",
    fg="white",
    relief="flat",
    cursor="hand2"
)

encrypt_button.pack(pady=10)


# Decrypt (Phase 2)

decrypt_button = tk.Button(
    root,
    text="🔓 Decrypt File",
    command=decrypt_file,
    font=("Arial", 12, "bold"),
    width=32,
    height=2,
    bg="#f59e0b",
    fg="white",
    relief="flat",
    cursor="hand2"
)

decrypt_button.pack(pady=10)


# Information

info = tk.Label(
    root,
    text="Generate a key → Encrypt → Keep the key safe → Decrypt",
    font=("Arial", 10),
    fg="#fbbf24",
    bg="#101827"
)

info.pack(pady=25)


root.mainloop()
