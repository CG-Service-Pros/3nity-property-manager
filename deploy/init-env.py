#!/usr/bin/env python3
"""Generate host-only secrets without printing them or overwriting existing state."""
import os
import secrets
from pathlib import Path

target = Path(__file__).with_name('.env')
keys = ['MONGO_PASSWORD', 'REDIS_PASSWORD', 'ACCESS_TOKEN_SECRET',
        'REFRESH_TOKEN_SECRET', 'RESET_TOKEN_SECRET', 'APPCREDZ_TOKEN_SECRET',
        'CIPHER_KEY', 'CIPHER_IV_KEY']
fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, 'w') as stream:
    stream.write(''.join(f'{key}={secrets.token_hex(32)}\n' for key in keys))
print('Generated deploy/.env with mode 0600; values are not displayed.')
