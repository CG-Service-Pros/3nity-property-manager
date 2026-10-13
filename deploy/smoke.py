#!/usr/bin/env python3
"""Synthetic API checks. Read credentials privately; print only status summaries."""
import json
import urllib.request
import urllib.error
import uuid
from pathlib import Path

root=Path(__file__).resolve().parent.parent
credentials=json.loads((root.parent/'operator-credentials.json').read_text())
base='http://127.0.0.1:8088'
def call(method,path,body=None,token=None,organization=None):
    headers={'Content-Type':'application/json'}
    if token: headers['Authorization']='Bearer '+token
    if organization: headers['organizationid']=organization
    req=urllib.request.Request(base+path,data=json.dumps(body).encode() if body is not None else None,headers=headers,method=method)
    try:
        with urllib.request.urlopen(req,timeout=20) as response:
            raw=response.read()
            return response.status,json.loads(raw) if raw and response.headers.get('Content-Type','').startswith('application/json') else None
    except urllib.error.HTTPError as error:
        return error.code,None

assert call('GET','/health')[0]==200
assert call('GET','/landlord')[0]==200
assert call('GET','/api/v2/properties')[0]==401
assert call('POST','/api/v2/authenticator/landlord/signup',{})[0]==404
status,login=call('POST','/api/v2/authenticator/landlord/signin',{'email':credentials['email'],'password':credentials['password']})
assert status==200
admin=login['accessToken']
status,reader=call('POST','/api/v2/authenticator/landlord/signin',{'clientId':credentials['clientId'],'clientSecret':credentials['clientSecret']})
assert status==200 and reader['organizationId']==credentials['organizationId']
read_token=reader['accessToken']
org=credentials['organizationId']
status,before=call('GET','/api/v2/properties',token=read_token,organization=org)
assert status==200 and isinstance(before,list)
for method,path in [('GET','/realms'),('POST','/properties'),('PATCH','/rents/payment/invalid/202610'),('DELETE','/properties/invalid'),('POST','/emails'),('POST','/templates')]:
    assert call(method,'/api/v2'+path,{},read_token,org)[0]==403,(method,path)
status,realm=call('POST','/api/v2/realms',{
    'name':'SYNTHETIC ACCEPTANCE '+str(uuid.uuid4()),'currency':'USD','locale':'en-US',
    'members':[{'email':credentials['email'],'name':'Test operator','role':'administrator','registered':True}],
    'applications':[]
},admin)
assert status==200
test_org=realm['_id']
status,property_record=call('POST','/api/v2/properties',{
    'name':'SYNTHETIC TEST UNIT','type':'house','surface':100,'price':1000,
    'address':{'street1':'123 Example Street','city':'Example','zipCode':'00000','country':'US'}
},admin,test_org)
assert status==200
status,records=call('GET','/api/v2/properties',token=admin,organization=test_org)
assert status==200 and any(p['name']=='SYNTHETIC TEST UNIT' for p in records)
assert call('GET','/api/v2/properties',token=read_token,organization=test_org)[0]==404
assert call('GET','/api/v2/properties',token=read_token,organization=org)[1]==before
print('PASS: gateway/UI health, authenticated property creation/read, closed signup, anonymous denial, read-only write/config denial, cross-organization denial, unchanged primary records.')
print('Synthetic fixture remains isolated in a clearly named acceptance organization; no real portfolio imported.')
