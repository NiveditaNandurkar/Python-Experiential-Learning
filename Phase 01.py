import os
import tkinter as tk
from tkinter import messagebox


KEY_FILE = "secret.key"


# ---------------- KEY GENERATION ----------------

def generate_key():
    key = os.urandom(32)

    with open(KEY_FILE, "wb") as file:
        file.write(key)

    messagebox.showinfo(
        "Success",
        "Secret key generated successfully!\n\n"
        "Keep secret.key safe."
    )


# ---------------- LOAD KEY ----------------

def load_key():
    if not os.path.exists(KEY_FILE):
        messagebox.showerror(
            "Error",
            "secret.key not found!\nPlease generate a key first."
        )
        return None

    with open(KEY_FILE, "rb") as file:
        return file.read()


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


root.mainloop()
