import json
from datetime import datetime, timedelta, timezone
from jwt import (
     JWT,
     jwk_from_dict,
     jwk_from_pem
)
from jwt.utils import get_int_from_datetime

instance = JWT()

message = {
    'iss':'https://example.com/',
    'sub':'yosida95',
    'iat': get_int_from_datetime(datetime.now(timezone.utc)),
    'exp': get_int_from_datetime(
        datetime.now(timezone.utc) + timedelta(hours=1))
}

# Load a RSA key from a JWK dict.
signing_key = jwk_from_dict({
    'kty': 'RSA',
    'e': 'AQAB',
    'n': '...',
    'd':'...'
})
# Or load a RSA key from a PEM file.
with open('rsa_private_key.json', 'r') as fh:
    verifying_key = jwk_from_dict(json.load(fh))
    
message_received = instance.decode(compact_jws, verifying_key, do_time_check=True)    

"""
Successfuly retrieved the `message` from the `compact_jws`
"""
assert message == message_received



