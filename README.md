# FileLocker

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-web%20app-000000?logo=flask&logoColor=white)
![Cryptography](https://img.shields.io/badge/Cryptography-Fernet-6A5ACD)
![Status](https://img.shields.io/badge/status-local%20development-blue)

FileLocker is a browser-based application for encrypting and decrypting files with a secret code you choose or one generated for you. It combines PBKDF2-HMAC-SHA256 key derivation with Fernet authenticated encryption, then returns the result as a download.

> **Important:** Keep the exact secret code used to encrypt a file. FileLocker does not store or recover codes. If you lose the code, you will not be able to decrypt that file.
>
> The current embedded page is branded **KeyVault**; **FileLocker** is the project name used in this documentation.

## Table of contents

- [Features](#features)
- [Technology stack](#technology-stack)
- [Screenshots](#screenshots)
- [How FileLocker works](#how-filelocker-works)
- [Encryption and decryption workflow](#encryption-and-decryption-workflow)
- [Secret codes](#secret-codes)
- [Project architecture](#project-architecture)
- [Project folder structure](#project-folder-structure)
- [Installation on Windows and VS Code](#installation-on-windows-and-vs-code)
- [Create a virtual environment](#create-a-virtual-environment)
- [Install dependencies](#install-dependencies)
- [Run locally](#run-locally)
- [Usage](#usage)
- [Security and privacy](#security-and-privacy)
- [Troubleshooting](#troubleshooting)
- [Production deployment](#production-deployment)
- [Future enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- Encrypt and decrypt files from a browser.
- Use a custom secret code or generate a random 20-character code.
- Random codes use Python's `secrets` module and include letters, numbers, and selected symbols.
- Show or hide the entered code, and copy a generated code.
- Drag and drop a file into the upload area, or browse to select one.
- Download the encrypted or decrypted result.
- Derive a Fernet key with PBKDF2-HMAC-SHA256 using 600,000 iterations and a fresh 16-byte random salt for each encryption.
- Limit uploads to 25 MB (25 MiB in the server's byte-based configuration).
- Display progress state, validation errors, and success messages in a responsive dark interface.
- Process file contents in memory in the application; it does not save uploaded or processed files to an application-managed permanent file store.

## Technology stack

- **Python** — application language
- **Flask** — web server, routes, and embedded page rendering
- **Python Cryptography** — PBKDF2-HMAC-SHA256 and Fernet
- **HTML, CSS, and JavaScript** — browser interface, embedded in the Python source

## Screenshots

Add screenshots here when they are available. The placeholders below intentionally do not represent actual screenshots.

<!-- Replace these placeholders with screenshots captured from the running application. -->

| Main page | Encryption workflow |
| --- | --- |
| `[Screenshot placeholder]` | `[Screenshot placeholder]` |

| Decryption workflow |
| --- |
| `[Screenshot placeholder]` |

## How FileLocker works

The browser sends the selected file and secret code to the Flask application. For encryption, the app creates a random salt, derives a 32-byte key from the secret code and salt, and encrypts the file bytes with Fernet. The response is sent as a file download. Decryption reads the salt from the encrypted file, derives the key again from the supplied code, and asks Fernet to authenticate and decrypt the data.

The encrypted file format is:

```text
KV1 marker (3 bytes) + random salt (16 bytes) + Fernet token
```

The marker identifies this application's current file format; the salt is not secret and is stored with the encrypted data. A wrong code or an invalid/tampered encrypted file fails Fernet authentication and cannot produce the original file.

## Encryption and decryption workflow

### Encrypt

1. Select a file up to 25 MB.
2. Enter a custom secret code or generate one.
3. Save the code somewhere secure before continuing.
4. Select **Encrypt file** and submit.
5. Download the resulting file, named with the `.encrypted` suffix.

### Decrypt

1. Select the `.encrypted` file.
2. Enter the exact same secret code used for encryption.
3. Select **Decrypt file** and submit.
4. Download the restored file.

FileLocker does not keep a copy of the secret code for recovery. The same code is required every time you decrypt that file.

## Secret codes

You can provide your own secret code, including names, numbers, letters, and symbols, or generate a random code in the interface. The backend accepts codes up to 1,024 characters. The browser trims surrounding whitespace before sending the code, so whitespace at the beginning or end is not part of the code sent by the current UI.

Generated codes are 20 characters long and are created on the server using Python's cryptographically secure `secrets.choice`. Save a generated code before encrypting; the application does not maintain a recoverable key vault.

For a custom code, choose a long, unique passphrase rather than a short or reused password. Key derivation makes guessing more expensive, but cannot make a weak code strong.

## Project architecture

```text
┌──────────────────────────────┐
│ Browser                      │
│ Embedded HTML/CSS/JavaScript │
└──────────────┬───────────────┘
               │ file + secret code (HTTP)
               ▼
┌──────────────────────────────┐
│ Flask app (exp.py)           │
│ /, /api/generate-key         │
│ /api/encrypt, /api/decrypt   │
└──────────────┬───────────────┘
               │ in-memory bytes
               ▼
┌──────────────────────────────┐
│ Cryptography                 │
│ PBKDF2-HMAC-SHA256 → Fernet  │
└──────────────┬───────────────┘
               │ downloadable response
               ▼
┌──────────────────────────────┐
│ Browser downloads result     │
└──────────────────────────────┘
```

The interface and server-side routes are in one Python file; there is no separate templates or static-assets directory in the current project.

## Project folder structure

```text
FileLocker/
├── exp.py       # Flask application, crypto functions, and embedded UI
├── README.md
└── .venv/       # Local virtual environment; create it during setup
```

The `.venv/` folder is generated locally and should not be committed.

## Installation on Windows and VS Code

### Prerequisites

- Windows 10 or later
- Python 3.9 or later, available from [python.org](https://www.python.org/downloads/) or the Microsoft Store
- Visual Studio Code (recommended) with the Microsoft Python extension
- Git, if you are cloning the repository

Check that Python is available from PowerShell:

```powershell
py --version
```

Open the project folder in VS Code using **File → Open Folder**. Open its integrated terminal with **Terminal → New Terminal**, and run the remaining commands from the folder containing `exp.py`.

## Create a virtual environment

In the VS Code PowerShell terminal:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, either allow scripts for your current user:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again, or use Command Prompt instead:

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

In VS Code, choose the `.venv` interpreter when prompted, or open the Command Palette (`Ctrl+Shift+P`), choose **Python: Select Interpreter**, and select the interpreter under `.venv`.

## Install dependencies

With the virtual environment activated:

```powershell
python -m pip install --upgrade pip
python -m pip install Flask cryptography
```

These are the third-party packages imported by the current application. The repository does not currently include a dependency lock file or `requirements.txt`.

## Run locally

From the folder containing `exp.py`, start the development server:

```powershell
python exp.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. Stop the server with `Ctrl+C` in the terminal.

The current `app.run(debug=True)` is for local development only. Do not expose this development server or its debugger to a network or the public internet.

## Usage

1. Open the local application in a browser.
2. Choose **Encrypt file** or **Decrypt file**.
3. Drop a file onto the upload area or select one from your device. The maximum upload size is 25 MB.
4. Enter a custom secret code or choose **Generate key**.
5. If you generated a key, use the copy control and store it safely. You can use the show/hide control to check the code.
6. Submit the operation and wait for the success or error message.
7. Save the downloaded result. For decryption, use the exact code from the encryption step.

The app's current download names are based on the uploaded filename: encryption adds `.encrypted`; decryption removes that suffix when present and prepends `decrypted_`.

## Security and privacy

- **The secret code is essential.** There is no password reset or recovery mechanism. Losing the code means losing access to the encrypted file.
- **Choose a strong code.** A salt prevents precomputed attacks across files, and PBKDF2 slows attempts, but short or guessable codes remain vulnerable to offline guessing.
- **Each encryption uses a random salt.** The salt is included in the output file because it is needed to derive the same key during decryption; it is not the secret.
- **Fernet authenticates encrypted data.** Invalid codes and modifications to the token cause decryption to fail.
- **The application does not save files to an application-managed permanent file store.** File contents are read into memory and the result is returned as a download. The underlying web stack or hosting environment may use temporary storage while receiving uploads; this is not a guarantee that no transient copies exist.
- **A hosted instance receives the uploaded data and secret code.** Only run a server you trust. If you deploy this app, use HTTPS and protect the server and its logs.
- **The local server is not production hardened.** Debug mode is enabled by the current source. Do not use Flask's development server for public deployment.
- **Keep backups of important originals and encrypted files.** FileLocker is a small utility, not a substitute for a managed backup or key-management system.

## Troubleshooting

| Problem | What to try |
| --- | --- |
| `py` or `python` is not recognized | Install Python and enable the option to add it to `PATH`, then reopen the terminal. |
| `ModuleNotFoundError: No module named 'flask'` or `'cryptography'` | Activate `.venv` and run `python -m pip install Flask cryptography`. |
| PowerShell refuses to activate `.venv` | Use the current-user execution policy command above, or activate the environment from Command Prompt. |
| The browser cannot connect | Confirm `python exp.py` is still running and visit `http://127.0.0.1:5000`. |
| Upload is rejected as too large | Choose a smaller file. The app's maximum request size is 25 MiB, and request encoding can make the effective file limit slightly lower near the boundary. |
| Decryption reports an incorrect key or invalid file | Check that the file is a FileLocker `.encrypted` download and enter the exact same code. A lost code cannot be recovered. |
| Copying a code does not work | Clipboard access may be restricted by the browser; the app selects the code so it can be copied manually. |

## Production deployment

The current source is intended for local development: it starts Flask with `debug=True`, has no production configuration, and contains no deployment or key-management setup. Do not deploy it publicly as-is.

Before considering a production deployment:

1. Disable debug mode and use a production WSGI server (for example, Waitress for a Windows host).
2. Put the service behind HTTPS and restrict who can access it.
3. Review upload handling, memory use, request timeouts, rate limiting, logging, and temporary-file behavior for your hosting platform.
4. Avoid logging secret codes or file contents, and define a retention policy for any temporary request data.
5. Configure and test operational monitoring and error handling without exposing debug traces.
6. Test large files and concurrent requests under realistic resource limits.

For a basic private Windows deployment with Waitress installed, the WSGI entry point would be `exp:app`; a command such as the following binds only to the local machine:

```powershell
python -m pip install waitress
waitress-serve --listen=127.0.0.1:8000 exp:app
```

This command alone does **not** make the app production-ready or provide HTTPS. Follow Waitress and your hosting platform's deployment guidance before making a service reachable by other users.

## Future enhancements

Possible future work, not currently implemented:

- Split the embedded page into template and static files.
- Add automated tests for encryption, decryption, invalid codes, and upload limits.
- Add dependency and environment manifests.
- Add deployment configuration with debug disabled by default.
- Add accessible UI improvements and a dedicated status for key-saving reminders.
- Add a documented, versioned file format and migration strategy.

## Contributing

Contributions are welcome. Before opening a pull request:

1. Create a focused change and explain its purpose.
2. Test locally with both encryption and decryption, including an incorrect code and an oversized upload.
3. Do not include real confidential files or secret codes in commits, screenshots, logs, or issue reports.
4. Update this README when setup instructions or implemented behavior changes.

## License

No license is currently specified in the project files. Until a license is added, do not assume that the source is available for reuse, modification, or redistribution. Add a `LICENSE` file with the intended license before publishing the project for reuse.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) for the Python web framework.
- [Python Cryptographic Authority](https://cryptography.io/) for the Cryptography library and Fernet implementation.
- [Shields.io](https://shields.io/) for the README badges.
