#!/usr/bin/env python3
"""Provision the local operator and MCP reader; retain secrets only on the host."""
import json
import os
import secrets
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent.parent
target = root.parent / 'operator-credentials.json'
if target.exists():
    raise SystemExit('Credentials already exist; refusing to overwrite or reprovision.')
password = secrets.token_urlsafe(32)
command = ['docker','compose','--env-file','deploy/.env','-f','deploy/compose.yaml',
           'exec','-T','-e','OPERATOR_PASSWORD','api','node','--input-type=module']
result = subprocess.run(command,cwd=root,input=(root/'deploy/bootstrap.mjs').read_text(),
                        env={**os.environ,'OPERATOR_PASSWORD':password},
                        capture_output=True,text=True)
if result.returncode:
    raise SystemExit('Bootstrap failed. Inspect the local process without exposing credential output.')
try:
    data=json.loads(result.stdout.strip().splitlines()[-1])
except Exception:
    raise SystemExit('Bootstrap returned unexpected output; verify stored state before retrying.')
fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'w') as stream: json.dump(data,stream)
with (root/'deploy/.env').open('a') as stream:
    stream.write(''.join(f'{key}={data[value]}\n' for key,value in [
        ('MCP_CLIENT_ID','clientId'),('MCP_CLIENT_SECRET','clientSecret'),('MCP_ORGANIZATION_ID','organizationId')]))
print(f'Provisioned local operator and read-only MCP principal. Secrets saved to {target}, mode 0600.')
