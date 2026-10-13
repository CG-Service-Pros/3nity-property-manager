import test from 'node:test';
import assert from 'node:assert/strict';
import {RentalReader} from './client.mjs';
const options={baseUrl:'http://localhost',clientId:'synthetic',clientSecret:'synthetic-secret',organizationId:'org-a'};

test('organization mismatch fails before any records are read', async()=>{
  let count=0;
  const api=new RentalReader({...options,fetchImpl:async()=>{count++;return Response.json({organizationId:'org-b',accessToken:'synthetic-token'});}});
  await assert.rejects(api.get('/properties'),/binding failed/);
  assert.equal(count,1);
});
test('write/configuration/arbitrary paths never reach the network',async()=>{
  const api=new RentalReader({...options,fetchImpl:async()=>{throw new Error('network must not be used');}});
  for(const path of ['/realms','/emails','/properties/id','/rents/payment/id/2026','/properties?url=http://evil']) {
    await assert.rejects(api.get(path),/not an MCP read tool/);
  }
});
test('GET binds organization and handles one expired token retry',async()=>{
  let auths=0, reads=0;
  const api=new RentalReader({...options,fetchImpl:async(url,request)=>{
    if(url.endsWith('/signin')) {auths++;return Response.json({organizationId:'org-a',accessToken:'synthetic-token'});}
    assert.equal(request.method,'GET');
    assert.equal(request.headers.organizationid,'org-a');
    reads++;
    return reads===1 ? new Response('',{status:401}) : Response.json([{name:'Synthetic property'}]);
  }});
  assert.deepEqual(await api.get('/properties'),[{name:'Synthetic property'}]);
  assert.equal(auths,2);
  assert.equal(reads,2);
});
test('oversize tool response is rejected',async()=>{
  const api=new RentalReader({...options,fetchImpl:async(url)=>url.endsWith('/signin')
    ? Response.json({organizationId:'org-a',accessToken:'synthetic-token'})
    : Response.json({payload:'x'.repeat(512001)})});
  await assert.rejects(api.get('/properties'),/size limit/);
});
