from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_der_public_key

BACKEND = default_backend()
ENCODING = Encoding.DER
KEY_FORMAT = PublicFormat.SubjectPublicKeyInfo
INFO = b'smokescreen handshake'
SHARED_KEY_LEN = 48

p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
g = 2

params_numbers = dh.DHParameterNumbers(p, g)
PARAMETERS = params_numbers.parameters(BACKEND)

def dhe_generate_key(parameters):
    return parameters.generate_private_key()

def dhe_serialize(key):
    return key.public_key().public_bytes(ENCODING, KEY_FORMAT)

def dhe_generated_shared(key, peer_key, length):
    shared_key = key.exchange(peer_key)
    return HKDF(algorithm=hashes.SHA256(),
        length=length,
        salt=None,
        info=INFO,
        backend=BACKEND).derive(shared_key)

def client_dhe_request():
    private_key = dhe_generate_key(PARAMETERS)
    public_key_ser = dhe_serialize(private_key)

    return private_key, public_key_ser

def server_dhe_response(client_req):
    client_key = load_der_public_key(client_req, backend=BACKEND)
    parameters = client_key.parameters()
    private_key = dhe_generate_key(parameters)
    public_key_ser = dhe_serialize(private_key)
    shared_key = dhe_generated_shared(private_key, client_key, SHARED_KEY_LEN)

    return shared_key, public_key_ser

def client_dhe_finish(private_key, server_resp):
    server_key = load_der_public_key(server_resp, backend=BACKEND)
    shared_key = dhe_generated_shared(private_key, server_key, SHARED_KEY_LEN)
    return shared_key

if __name__ == '__main__':
    client_priv, client_req = client_dhe_request()
    assert type(client_req) == bytes

    server_shared, server_resp = server_dhe_response(client_req)
    assert type(server_resp) == bytes

    client_shared = client_dhe_finish(client_priv, server_resp)
    assert server_shared == client_shared
