import subprocess
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, utils

# --- CONFIGURATION ---
STUDENT_PRIVATE_KEY = "student_private.pem"
INSTRUCTOR_PUBLIC_KEY = "instructor_public.pem"

def main():
    print("🔹 Generating Cryptographic Proof...")

    # 1. Get the latest Git Commit Hash
    try:
        commit_hash = subprocess.check_output(["git", "log", "-1", "--format=%H"]).decode().strip()
        if len(commit_hash) != 40:
            raise ValueError("Invalid commit hash length")
        print(f"✅ Commit Hash: {commit_hash}")
    except Exception as e:
        print(f"❌ Error getting git commit hash: {e}")
        print("   Are you in the git repository? Did you commit your changes?")
        return

    # 2. Load Student Private Key
    try:
        with open(STUDENT_PRIVATE_KEY, "rb") as f:
            student_key = serialization.load_pem_private_key(f.read(), password=None)
    except FileNotFoundError:
        print(f"❌ Error: {STUDENT_PRIVATE_KEY} not found.")
        return

    # 3. Load Instructor Public Key
    try:
        with open(INSTRUCTOR_PUBLIC_KEY, "rb") as f:
            instructor_key = serialization.load_pem_public_key(f.read())
    except FileNotFoundError:
        print(f"❌ Error: {INSTRUCTOR_PUBLIC_KEY} not found.")
        return

    # 4. Sign the Commit Hash (RSA-PSS)
    # CRITICAL: We sign the ASCII bytes of the hash string, NOT the binary representation
    message = commit_hash.encode('utf-8')
    
    signature = student_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("✅ Signed commit hash with Student Private Key")

    # 5. Encrypt the Signature (RSA-OAEP)
    encrypted_signature = instructor_key.encrypt(
        signature,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print("✅ Encrypted signature with Instructor Public Key")

    # 6. Encode to Base64
    final_proof = base64.b64encode(encrypted_signature).decode('utf-8')

    # 7. Output Results
    print("\n" + "="*50)
    print("📜 SUBMISSION DATA (COPY THESE EXACTLY)")
    print("="*50)
    print(f"\n1. Commit Hash:\n{commit_hash}")
    print(f"\n2. Encrypted Commit Signature (One Line):\n{final_proof}")
    print("\n" + "="*50)

if __name__ == "__main__":
    main()
