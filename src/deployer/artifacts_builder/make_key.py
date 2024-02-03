import os

def make_public_private_key_pair(key_algorithm, size, path_public, path_private):
    print(f'creating public/private key pair at {path_public} and {path_private}')
    pub_exists = os.path.exists(path_public)
    priv_exists = os.path.exists(path_private)
    if pub_exists and priv_exists:
        print('public and private keys already exist, skipping')
        return
    # If only one of the keys exists, recreate both
    if pub_exists or priv_exists:
        print('only one of the keys exists, recreating both')
        try:
            os.remove(path_public)
        except FileNotFoundError:
            pass
        try:
            os.remove(path_private)
        except FileNotFoundError:
            pass
    # Create the directory if it does not exist
    os.makedirs(os.path.dirname(path_public), exist_ok=True)
    os.makedirs(os.path.dirname(path_private), exist_ok=True)
    # Create the keys
    if key_algorithm.lower() == 'rsa':
        os.system(f'openssl genpkey -algorithm RSA -out {path_private} -pkeyopt rsa_keygen_bits:{size}')
        os.system(f'openssl rsa -pubout -in {path_private} -out {path_public}')
    else:
        print(f'Unsupported key algorithm: {key_algorithm}')