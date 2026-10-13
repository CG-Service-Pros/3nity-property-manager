// Run inside the API image with a host-generated OPERATOR_PASSWORD. Capture
// stdout directly into a mode-0600 credential file; never display it in a chat.
import mongoose from 'mongoose';
import jwt from 'jsonwebtoken';
import crypto from 'node:crypto';
import {Collections} from '@microrealestate/common';

if (!process.env.OPERATOR_PASSWORD || !process.env.APPCREDZ_TOKEN_SECRET) {
  throw new Error('Missing bootstrap configuration');
}
await mongoose.connect(process.env.MONGO_URL);
const email = 'operator@3nity.local';
if (await Collections.Realm.findOne({name:'3nity Ventures'})) {
  throw new Error('Organization already exists; bootstrap will not overwrite credentials');
}
if (!await Collections.Account.findOne({email})) {
  await Collections.Account.create({firstname:'3nity',lastname:'Operator',email,password:process.env.OPERATOR_PASSWORD});
}
const realm = new Collections.Realm({
  name:'3nity Ventures',currency:'USD',locale:'en-US',
  members:[{email,name:'3nity Operator',role:'administrator',registered:true}],
  isCompany:true, companyInfo:{name:'3nity Ventures'}, applications:[]
});
const clientId = crypto.randomUUID();
const expiryDate = new Date(Date.now()+90*24*3600*1000);
const clientSecret = jwt.sign({organizationId:String(realm._id),jti:clientId,exp:Math.floor(expiryDate.getTime()/1000)},process.env.APPCREDZ_TOKEN_SECRET);
realm.applications.push({name:'MCP Reader',role:'read_only',clientId,clientSecret,expiryDate});
await realm.save();
await mongoose.disconnect();
console.log(JSON.stringify({email,password:process.env.OPERATOR_PASSWORD,organizationId:String(realm._id),clientId,clientSecret}));
