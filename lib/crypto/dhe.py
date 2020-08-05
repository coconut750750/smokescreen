from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, ParameterFormat, load_der_public_key, load_der_parameters

KEY_SIZE = 512
G = 2
BACKEND = default_backend()
ENCODING = Encoding.DER
PARAM_FORMAT = ParameterFormat.PKCS3
KEY_FORMAT = PublicFormat.SubjectPublicKeyInfo
INFO = b'smokescreen handshake'
SHARED_KEY_LEN = 48

def dhe_generate_params():
    parameters = dh.generate_parameters(generator=G, key_size=KEY_SIZE, backend=BACKEND)
    return parameters.parameter_bytes(ENCODING, PARAM_FORMAT)

def dhe_generate_key(params_serialized):
    dh_params = load_der_parameters(params_serialized, backend=BACKEND)
    return dh_params.generate_private_key()

def dhe_serialize(key):
    return key.public_key().public_bytes(ENCODING, KEY_FORMAT)

def dhe_generated_shared(key, peer_serialized, length):
    peer_key = load_der_public_key(peer_serialized, backend=BACKEND)
    shared_key = key.exchange(peer_key)
    return HKDF(algorithm=hashes.SHA256(),
        length=length,
        salt=None,
        info=INFO,
        backend=BACKEND).derive(shared_key)

def format_client_request(params_ser, public_key_ser):
    params_len = len(params_ser)
    return f'{params_len}\n'.encode() + params_ser + public_key_ser

def extract_from_client_request(request):
    params_len = request.split(b'\n')[0].decode()
    params_start = len(params_len) + 1 # +1 because of new line
    key_start = params_start + int(params_len)
    params_ser = request[params_start: key_start]
    key_ser = request[key_start:]

    return params_ser, key_ser

def client_dhe_request():
    params_ser = dhe_generate_params()
    private_key = dhe_generate_key(params_ser)
    public_key_ser = dhe_serialize(private_key)

    return private_key, format_client_request(params_ser, public_key_ser)

def server_dhe_response(client_req):
    params_ser, client_key_ser = extract_from_client_request(client_req)
    private_key = dhe_generate_key(params_ser)
    public_key_ser = dhe_serialize(private_key)
    shared_key = dhe_generated_shared(private_key, client_key_ser, SHARED_KEY_LEN)

    return shared_key, public_key_ser

def client_dhe_finish(private_key, server_resp):
    shared_key = dhe_generated_shared(private_key, server_resp, SHARED_KEY_LEN)
    return shared_key

if __name__ == '__main__':
    client_priv, client_req = client_dhe_request()
    assert type(client_req) == bytes

    server_shared, server_resp = server_dhe_response(client_req)
    assert type(server_resp) == bytes

    client_shared = client_dhe_finish(client_priv, server_resp)
    assert server_shared == client_shared
