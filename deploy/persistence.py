#!/usr/bin/env python3
"""Staging-only Mongo recreation, backup and isolated restore verification."""
import hashlib
import json
import os
import subprocess
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

root=Path(__file__).resolve().parent.parent
env={}
for line in (root/'deploy/.env').read_text().splitlines():
    if '=' in line: key,value=line.split('=',1); env[key]=value
compose=['docker','compose','--env-file','deploy/.env','-f','deploy/compose.yaml']
def run(command, data=None):
    result=subprocess.run(command,cwd=root,input=data,capture_output=True)
    if result.returncode: raise RuntimeError('Persistence verification command failed; inspect the host privately.')
    return result.stdout
def live_command(container, program):
    return ['docker','exec',container,'mongosh','--quiet','--username','root','--password',env['MONGO_PASSWORD'],'--authenticationDatabase','admin','trinity','--eval',program]
def snapshot(container, authenticated=True):
    program='const r={}; for(const n of db.getCollectionNames().sort()){r[n]=db.getCollection(n).find().sort({_id:1}).toArray();} print(EJSON.stringify(r));'
    command=live_command(container,program) if authenticated else ['docker','exec',container,'mongosh','--quiet','trinity','--eval',program]
    data=json.loads(run(command).decode().strip())
    digest=hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return digest,{name:len(rows) for name,rows in data.items()}
mongo=run(compose+['ps','-q','mongo']).decode().strip()
guard='print(db.properties.countDocuments({realmId:'+json.dumps(env['MCP_ORGANIZATION_ID'])+'})+db.occupants.countDocuments({realmId:'+json.dumps(env['MCP_ORGANIZATION_ID'])+'})+db.notes.countDocuments({realmId:'+json.dumps(env['MCP_ORGANIZATION_ID'])+'}));'
if int(run(live_command(mongo,guard)).decode().strip()) != 0:
    raise SystemExit('Refusing disruption: the primary organization is no longer an empty staging fixture.')
before,counts=snapshot(mongo)
backups=root.parent/'backups'; backups.mkdir(mode=0o700,exist_ok=True); backups.chmod(0o700)
archive=backups/('staging-'+datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%SZ')+'.archive.gz')
command=['docker','exec',mongo,'mongodump','--username','root','--password',env['MONGO_PASSWORD'],'--authenticationDatabase','admin','--db','trinity','--archive','--gzip','--quiet']
content=run(command)
fd=os.open(archive,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'wb') as stream: stream.write(content)
run(compose+['up','-d','--no-build','--force-recreate','mongo'])
mongo=run(compose+['ps','-q','mongo']).decode().strip()
for attempt in range(30):
    try:
        after,_=snapshot(mongo); break
    except RuntimeError:
        if attempt==29: raise
        time.sleep(1)
assert before==after,'Persistent-volume snapshot changed after Mongo recreation'
temporary='trinity-restore-'+uuid.uuid4().hex[:10]
try:
    run(['docker','run','-d','--name',temporary,'--network','none','--memory','512m','--cpus','1','mongo:7','--wiredTigerCacheSizeGB','0.25'])
    for attempt in range(30):
        try:
            run(['docker','exec',temporary,'mongosh','--quiet','--eval','db.adminCommand({ping:1})']); break
        except RuntimeError:
            if attempt==29: raise
            time.sleep(1)
    run(['docker','exec','-i',temporary,'mongorestore','--archive','--gzip','--quiet'],content)
    restored,_=snapshot(temporary,authenticated=False)
    assert before==restored,'Isolated backup restore changed the document snapshot'
finally:
    run(['docker','rm','-f','-v',temporary])
print(json.dumps({'persistence':'PASS','isolated_restore':'PASS','document_hash':before,'collections':counts,'backup':str(archive),'scope':'synthetic staging data; Mongo backup only'}))
