import base64
import hashlib
import re

import ecdsa
from .errors import PrivateKeyParseError
from ecdsa.keys import BadSignatureError


def format_private_key(private_key):
    private_key = private_key.strip()
    x = re.sub(r"\n*-----[A-Z]* [A-Z]* [A-Z]* [A-Z]*-----\n*", "", private_key)
    pr_key = str(x)
    return pr_key


def sign_dataset(private_key: str, dataset: str):
    formatted_pk = format_private_key(private_key)
    sk = ecdsa.SigningKey.from_der(base64.b64decode(formatted_pk))
    dataset = dataset.encode("utf-8")
    sig = sk.sign(dataset, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_der)
    return base64.b64encode(sig).decode("utf-8")


def sign_dataset_using_privatekey_file(private_key_path: str, dataset: str):
    with open(private_key_path) as file:
        sk = ecdsa.SigningKey.from_pem(file.read())
    dataset = dataset.encode("utf-8")
    sig = sk.sign(dataset, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_der)
    return base64.b64encode(sig).decode("utf-8")


def employee_id(org_id: str, corp_email: str):
    emp_id = hashlib.sha256(f"corp:email:{org_id}:{corp_email}".encode()).hexdigest()
    return emp_id


def convert_to_valid_pem(private_key: str):
    if private_key.startswith("-----BEGIN"):
        return private_key
    pieces = []
    pieces.append("-----BEGIN EC PRIVATE KEY-----")
    last_idx = 0
    for x in range(64, len(private_key), 64):
        pieces.append(private_key[last_idx:x])
        last_idx = x
    pieces.append(private_key[last_idx:])
    pieces.append("-----END EC PRIVATE KEY-----")
    return "\n".join(pieces)


def verify_dataset(private_key: str, dataset: str, signature: str):
    try:
        private_key_pem = convert_to_valid_pem(private_key)
        sk = ecdsa.SigningKey.from_pem(private_key_pem)
        vk = sk.get_verifying_key()
        sig_bytes = base64.b64decode(signature)
        dataset = dataset.encode("utf-8")
        result = vk.verify(
            sig_bytes,
            dataset,
            hashfunc=hashlib.sha256,
            sigdecode=ecdsa.util.sigdecode_der,
        )
        return result
    except BadSignatureError:
        return False
    except Exception as _:
        raise PrivateKeyParseError(_)


def batch_list(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        yield lst[i : i + batch_size]
