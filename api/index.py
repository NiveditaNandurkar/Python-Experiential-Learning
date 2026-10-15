from flask import Flask, request, jsonify, send_file, render_template_string
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import secrets
from werkzeug.utils import secure_filename
from io import BytesIO

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 MB max


PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KeyVault | File Security</title>
<style>
:root{--bg:#080d19;--panel:#111a2d;--line:#2b3854;--text:#f2f5ff;--muted:#9aa8c0;--blue:#86a8ff;--purple:#ac96ff;--green:#82e5c5}
*{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(ellipse at 50% 0%,#24365e 0,transparent 55%),var(--bg);font-family:Inter,Segoe UI,Arial,sans-serif;color:var(--text)}
header{height:72px;padding:0 6%;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #ffffff12;background:#080d19bb;backdrop-filter:blur(12px)}
.brand{font-size:23px;font-weight:800;letter-spacing:-1px}.brand span{color:var(--blue)}.online{font-size:12px;color:#b8c4d9}.dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--green);margin-right:8px}
main{max-width:1100px;margin:auto;padding:0 22px}.hero{text-align:center;padding:48px 0 32px}.eyebrow{display:inline-block;padding:8px 13px;border:1px solid #8caaff38;border-radius:30px;background:#1b2b4b80;color:#b7c9ff;font-size:10px;font-weight:700;letter-spacing:1.4px}
h1{font-size:clamp(36px,5vw,54px);letter-spacing:-2px;margin:18px 0 10px}.gradient{background:linear-gradient(90deg,#8eb5ff,#c0a3ff);background-clip:text;-webkit-background-clip:text;color:transparent}
.hero p{max-width:590px;margin:0 auto;color:var(--muted);font-size:14px;line-height:1.8}.features{display:flex;justify-content:center;flex-wrap:wrap;gap:18px;margin-top:22px;color:#aab8d0;font-size:11px}
.layout{display:grid;grid-template-columns:1.4fr .85fr;gap:18px;align-items:start}.card{background:linear-gradient(145deg,#141e32,#0e1627);border:1px solid #ffffff14;border-radius:18px;box-shadow:0 18px 55px #0003}.main-card{padding:26px}.heading{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:22px}.kicker{font-size:9px;letter-spacing:1.5px;color:#9eb3e5;font-weight:800;margin-bottom:8px}h2{margin:0;font-size:23px}.badge{font-size:9px;color:var(--green);border:1px solid #64dcb42b;border-radius:7px;padding:8px}
.tabs{display:grid;grid-template-columns:1fr 1fr;gap:5px;padding:4px;background:#090f1d;border-radius:10px;margin-bottom:24px}.tab{border:0;border-radius:7px;background:transparent;color:#9ba8bf;padding:12px;font-size:12px;font-weight:700}.tab.active{background:#263858;color:#eef2ff}
.label{display:block;font-size:10px;letter-spacing:1.1px;font-weight:800;color:#c0cbe0;margin:0 0 10px}.drop{height:150px;border:1px dashed #596f95;border-radius:12px;background:#0b1425;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:9px;text-align:center;cursor:pointer;padding:15px;overflow:hidden}.drop:hover,.drop.drag{border-color:var(--blue);background:#172440}.drop input{display:none}.upload{width:36px;height:36px;display:grid;place-items:center;border-radius:10px;background:#243656;color:#b7caff;font-size:23px}.drop strong{font-size:12px;overflow-wrap:anywhere}.drop span{font-size:11px;color:#a0aec6}.drop small{font-size:9px;color:#7383a0}
.keyrow{display:flex;align-items:center;justify-content:space-between;margin-top:22px}.textbtn{border:0;background:transparent;color:#b5c5ff;font-size:11px;font-weight:700;padding:0 0 10px}
.keyinput{display:flex;border:1px solid var(--line);border-radius:9px;background:#090f1d;overflow:hidden}.keyinput:focus-within{border-color:var(--blue)}.keyinput input{min-width:0;width:100%;padding:13px;background:transparent;border:0;outline:0;color:#f0f3ff;font-family:Consolas,monospace;font-size:11px}.keyinput button{border:0;background:transparent;color:#b6c6ff;padding:0 13px;font-size:10px}
.hint{font-size:10px;color:#9aa8c0;line-height:1.7;margin:10px 0 18px}.primary{width:100%;display:flex;justify-content:space-between;align-items:center;padding:14px 16px;border:0;border-radius:9px;background:linear-gradient(100deg,#80a4ff,#a28af4);color:#0a1020;font-weight:800;font-size:12px}.primary:disabled{opacity:.6;cursor:wait}
.foot{border-top:1px solid #ffffff10;margin-top:20px;padding-top:15px;color:#8593ac;font-size:10px;line-height:1.6}.side{display:grid;gap:16px}.sidecard{padding:22px}.icon{width:38px;height:38px;border-radius:11px;display:grid;place-items:center;background:#2b2850;color:#c5b3ff;font-size:22px;margin-bottom:17px}.sidecard h3{font-size:18px;margin:0 0 9px}.sidecard p{font-size:11px;line-height:1.8;color:var(--muted)}
.keybox{display:flex;align-items:center;gap:8px;min-height:54px;padding:9px;border:1px solid #41385f;border-radius:9px;background:#0b1120}.keybox span{flex:1;min-width:0;overflow-wrap:anywhere;color:#c8baff;font:10px/1.6 Consolas,monospace}.keybox button{flex-shrink:0;border:1px solid #4b4773;border-radius:7px;background:#242341;color:#e0d9ff;padding:8px}.secondary{width:100%;margin-top:10px;padding:12px;border:1px solid #7667ba70;border-radius:9px;background:#292348;color:#e1d9ff;font-size:11px;font-weight:700}
.warning{display:flex;gap:9px;margin-top:17px;padding-top:14px;border-top:1px solid #ffffff10;color:#9aa8c0;font-size:10px;line-height:1.7}.warning b{color:#f1d59b}.steps{display:grid;gap:18px}.step{display:flex;gap:12px;align-items:flex-start}.num{flex-shrink:0;width:29px;height:29px;display:grid;place-items:center;border:1px solid #344866;border-radius:8px;background:#1b2a43;color:#b4c7ff;font-size:10px;font-weight:800}.step b{font-size:11px}.step p{margin:5px 0 0;font-size:10px}
.status{margin:0 0 15px;padding:11px 12px;border-radius:8px;font-size:11px;line-height:1.6}.status[hidden]{display:none}.success{background:#15382f;border:1px solid #2d7864;color:#b1f4dd}.error{background:#401f2b;border:1px solid #9a4554;color:#ffc0ca}.info{background:#1b2b48;border:1px solid #3d5c91;color:#c2d5ff}
footer{display:flex;justify-content:space-between;gap:12px;padding:26px 2px;color:#73819a;font-size:10px}
@media(max-width:760px){header{height:64px;padding:0 18px}.online{font-size:10px}main{padding:0 14px}.hero{padding:38px 0 26px}.layout{grid-template-columns:1fr}.main-card{padding:20px}.side{grid-template-columns:1fr}.features{gap:12px}footer{flex-direction:column}}
</style>
</head>
<body>
<header><div class="brand">⌁ Key<span>Vault</span></div><div class="online"><span class="dot"></span>Private file workspace</div></header>
<main>
<section class="hero">
<div class="eyebrow">✦ YOUR FILES. YOUR KEYS. YOUR CONTROL.</div>
<h1>Privacy, <span class="gradient">locked in.</span></h1>
<p>Encrypt sensitive files into unreadable data, then restore them with the exact same secret key.</p>
<div class="features"><span>◈ Authenticated encryption</span><span>✧ Secure key generator</span><span>⌁ Simple file recovery</span></div>
</section>
<section class="layout">
<div class="card main-card">
<div class="heading"><div><div class="kicker">FILE WORKSPACE</div><h2>Protect a file</h2></div><div class="badge">⌑ SECURE MODE</div></div>
<div class="tabs"><button class="tab active" id="encryptTab" data-mode="encrypt">↗ Encrypt file</button><button class="tab" id="decryptTab" data-mode="decrypt">↙ Decrypt file</button></div>
<form id="fileForm">
<label class="label" for="fileInput">SELECT FILE <span style="color:#71809c;font-weight:400">• Max 25 MB</span></label>
<label class="drop" id="dropzone" for="fileInput"><input id="fileInput" type="file" required><span class="upload">↑</span><strong id="fileTitle">Drop your file here</strong><span id="fileSubtitle">or browse files from your device</span><small>Any file type · Up to 25 MB</small></label>
<div class="keyrow"><label class="label" for="secretKey">SECRET KEY</label><button type="button" class="textbtn" id="generateKey">✧ Generate key</button></div>
<div class="keyinput"><input id="secretKey" type="password" autocomplete="off" placeholder="Enter your own code, e.g. MySecret@123" required><button type="button" id="toggleKey">Show</button></div>
<p class="hint">ⓘ Use the exact same secret code to decrypt your file. A lost code cannot be recovered.</p>
<div id="status" class="status" role="status" aria-live="polite" hidden></div>
<button type="submit" class="primary" id="submitBtn"><span id="submitText">Encrypt file securely</span><span>→</span></button>
</form>
<div class="foot">▣ Files are processed in memory and are not saved to an upload folder. Keep a backup of your secret code.</div>
</div>
<aside class="side">
<div class="card sidecard"><div class="icon">✧</div><div class="kicker">KEY GENERATOR</div><h3>Your own secret code</h3><p>Generate a random code, or type any name, numbers and symbols in the Secret Code field.</p>
<div class="keybox"><span id="generatedKeyText">Your key will appear here</span><button type="button" id="copyKey" disabled title="Copy key">▢</button></div>
<button type="button" class="secondary" id="generateKeySide">Generate random secret code ✧</button>
<div class="warning"><b>!</b><span><b>Important:</b> KeyVault cannot retrieve a lost key. Keep it somewhere safe and separate from your encrypted file.</span></div></div>
<div class="card sidecard"><div class="kicker">HOW IT WORKS</div><div class="steps">
<div class="step"><span class="num">01</span><div><b>Choose a file</b><p>Select the file you want to protect.</p></div></div>
<div class="step"><span class="num">02</span><div><b>Generate a key</b><p>Copy and safely save your secret key.</p></div></div>
<div class="step"><span class="num">03</span><div><b>Encrypt or decrypt</b><p>Download the resulting file.</p></div></div>
</div></div>
</aside>
</section>
<footer><span>KeyVault · Python student project</span><span>File encryption and decryption</span></footer>
</main>
<script>
const fileInput=document.getElementById("fileInput");
const dropzone=document.getElementById("dropzone");
const secretKey=document.getElementById("secretKey");
const statusBox=document.getElementById("status");
const submitBtn=document.getElementById("submitBtn");
let mode="encrypt",generatedKey="";
function showStatus(message,type="info"){statusBox.textContent=message;statusBox.className="status "+type;statusBox.hidden=false}
function hideStatus(){statusBox.hidden=true}
function setMode(nextMode){
 mode=nextMode;
 document.querySelectorAll(".tab").forEach(b=>{const active=b.dataset.mode===mode;b.classList.toggle("active",active);b.setAttribute("aria-selected",String(active))});
 document.getElementById("submitText").textContent=mode==="encrypt"?"Encrypt file securely":"Decrypt file securely";
 document.getElementById("fileTitle").textContent=mode==="encrypt"?"Drop your file here":"Drop your encrypted file here";
 document.getElementById("fileSubtitle").textContent="or browse files from your device";
 fileInput.value="";hideStatus();
}
document.querySelectorAll(".tab").forEach(b=>b.addEventListener("click",()=>setMode(b.dataset.mode)));
fileInput.addEventListener("change",()=>{const f=fileInput.files[0];if(f){document.getElementById("fileTitle").textContent=f.name;document.getElementById("fileSubtitle").textContent=(f.size/1048576).toFixed(2)+" MB · Ready to "+mode;hideStatus()}});
["dragenter","dragover"].forEach(n=>dropzone.addEventListener(n,e=>{e.preventDefault();dropzone.classList.add("drag")}));
["dragleave","drop"].forEach(n=>dropzone.addEventListener(n,e=>{e.preventDefault();dropzone.classList.remove("drag")}));
dropzone.addEventListener("drop",e=>{if(e.dataTransfer.files.length){fileInput.files=e.dataTransfer.files;fileInput.dispatchEvent(new Event("change"))}});
async function generateKey(){
 const buttons=[document.getElementById("generateKey"),document.getElementById("generateKeySide")];buttons.forEach(b=>b.disabled=true);
 try{
  const r=await fetch("/api/generate-key");if(!r.ok)throw new Error("Key generation failed.");
  const data=await r.json();generatedKey=data.key;
  document.getElementById("generatedKeyText").textContent=generatedKey;document.getElementById("copyKey").disabled=false;
  secretKey.value=generatedKey;secretKey.type="text";document.getElementById("toggleKey").textContent="Hide";
  showStatus("Secret code generated and added to the field. Save it before encrypting.","success");
 }catch(e){showStatus(e.message,"error")}finally{buttons.forEach(b=>b.disabled=false)}
}
document.getElementById("generateKey").addEventListener("click",generateKey);
document.getElementById("generateKeySide").addEventListener("click",generateKey);
document.getElementById("toggleKey").addEventListener("click",()=>{const visible=secretKey.type==="text";secretKey.type=visible?"password":"text";document.getElementById("toggleKey").textContent=visible?"Show":"Hide"});
document.getElementById("copyKey").addEventListener("click",async()=>{
 if(!generatedKey)return;
 try{await navigator.clipboard.writeText(generatedKey);showStatus("Secret code copied. Store it somewhere safe.","success")}
 catch(e){secretKey.focus();secretKey.select();showStatus("Clipboard blocked. The key is selected so you can copy it manually.","info")}
});
document.getElementById("fileForm").addEventListener("submit",async e=>{
 e.preventDefault();hideStatus();const file=fileInput.files[0];
 if(!file)return showStatus("Please choose a file first.","error");
 if(!secretKey.value.trim())return showStatus("Enter a key or generate one.","error");
 if(file.size>25*1024*1024)return showStatus("File exceeds the 25 MB limit.","error");
 const formData=new FormData();formData.append("file",file);formData.append("key",secretKey.value.trim());
 const text=document.getElementById("submitText"),oldText=text.textContent;submitBtn.disabled=true;text.textContent=mode==="encrypt"?"Encrypting file…":"Decrypting file…";
 try{
  const r=await fetch("/api/"+mode,{method:"POST",body:formData});
  if(!r.ok){let msg="Operation failed.";try{msg=(await r.json()).error||msg}catch{}throw new Error(msg)}
  const blob=await r.blob(),disposition=r.headers.get("Content-Disposition")||"",match=disposition.match(/filename="?([^";]+)"?/i);
  const filename=match?match[1]:(mode==="encrypt"?file.name+".encrypted":"decrypted_"+file.name);
  const url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download=filename;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  showStatus(mode==="encrypt"?"Encryption successful. Your encrypted file was downloaded.":"Decryption successful. Your restored file was downloaded.","success");
 }catch(err){showStatus(err.message||"Something went wrong.","error")}
 finally{submitBtn.disabled=false;text.textContent=oldText}
});
</script>
</body>
</html>
"""


def derive_fernet_key(secret_code, salt):
    """Derive a Fernet-compatible key from any user-entered secret code."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )
    raw_key = kdf.derive(secret_code.encode("utf-8"))
    return base64.urlsafe_b64encode(raw_key)


def encrypt_with_custom_code(data, secret_code):
    # A fresh random salt is stored with each encrypted file.
    salt = secrets.token_bytes(16)
    key = derive_fernet_key(secret_code, salt)
    token = Fernet(key).encrypt(data)
    # Prefix marker + salt + Fernet token.
    return b"KV1" + salt + token


def decrypt_with_custom_code(encrypted_data, secret_code):
    # Format: 3-byte marker + 16-byte salt + Fernet token.
    if len(encrypted_data) < 20 or encrypted_data[:3] != b"KV1":
        raise InvalidToken
    salt = encrypted_data[3:19]
    token = encrypted_data[19:]
    key = derive_fernet_key(secret_code, salt)
    return Fernet(key).decrypt(token)


@app.route("/")
def home():
    # The full browser UI (HTML, CSS, JavaScript) is embedded in this Python file.
    return render_template_string(PAGE)


@app.route("/api/generate-key", methods=["GET"])
def generate_key():
    # Generate a memorable custom secret code using a secure random source.
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%"
    code = "".join(secrets.choice(alphabet) for _ in range(20))
    return jsonify({"key": code})


@app.route("/api/encrypt", methods=["POST"])
def encrypt_file():
    uploaded = request.files.get("file")
    secret_code = request.form.get("key", "")

    if not uploaded or not uploaded.filename:
        return jsonify({"error": "Please choose a file to encrypt."}), 400
    if not secret_code.strip():
        return jsonify({"error": "Enter your own secret code or generate one."}), 400
    if len(secret_code) > 1024:
        return jsonify({"error": "Secret code must be 1024 characters or fewer."}), 400

    try:
        original_data = uploaded.read()
        encrypted_data = encrypt_with_custom_code(original_data, secret_code)
        filename = secure_filename(uploaded.filename) or "file"

        return send_file(
            BytesIO(encrypted_data),
            as_attachment=True,
            download_name=filename + ".encrypted",
            mimetype="application/octet-stream"
        )
    except Exception:
        app.logger.exception("Encryption failed")
        return jsonify({"error": "Encryption failed. Please try again."}), 500


@app.route("/api/decrypt", methods=["POST"])
def decrypt_file():
    uploaded = request.files.get("file")
    secret_code = request.form.get("key", "")

    if not uploaded or not uploaded.filename:
        return jsonify({"error": "Please choose an encrypted file to decrypt."}), 400
    if not secret_code.strip():
        return jsonify({"error": "Enter the same secret code used for encryption."}), 400
    if len(secret_code) > 1024:
        return jsonify({"error": "Secret code must be 1024 characters or fewer."}), 400

    try:
        encrypted_data = uploaded.read()
        decrypted_data = decrypt_with_custom_code(encrypted_data, secret_code)
        filename = secure_filename(uploaded.filename) or "file"

        if filename.endswith(".encrypted"):
            filename = filename[:-10]

        return send_file(
            BytesIO(decrypted_data),
            as_attachment=True,
            download_name="decrypted_" + filename,
            mimetype="application/octet-stream"
        )
    except InvalidToken:
        return jsonify({
            "error": "Decryption failed. The key is incorrect or the file is not a valid encrypted file."
        }), 400
    except Exception:
        app.logger.exception("Decryption failed")
        return jsonify({"error": "Could not decrypt this file. Check the file and key."}), 400


@app.errorhandler(413)
def file_too_large(_error):
    return jsonify({"error": "File exceeds the 25 MB upload limit."}), 413


if __name__ == "__main__":
    app.run(debug=True)
