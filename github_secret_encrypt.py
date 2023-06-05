import argparse
from base64 import b64encode
from nacl import encoding, public

def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    print(b64encode(encrypted).decode("utf-8"))

def main():
    parser = argparse.ArgumentParser(description='Encrypt the secret value using the GitHub public key.')
    parser.add_argument('-p', '--public_key', type=str, help='GitHub public key', required=True)
    parser.add_argument('-s', '--secret_value', type=str, help='Secret value', required=True)
    args = parser.parse_args()

    encrypt(args.public_key, args.secret_value)

if __name__ == "__main__":
    main()
